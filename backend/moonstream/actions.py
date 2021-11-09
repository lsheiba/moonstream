import json
import logging
from typing import Optional, Dict, Any
from enum import Enum
import uuid

import boto3  # type: ignore
from bugout.data import BugoutSearchResults
from bugout.exceptions import BugoutResponseException
from bugout.journal import SearchOrder
from ens.utils import is_valid_ens_name  # type: ignore
from eth_utils.address import is_address  # type: ignore
from moonstreamdb.models import (
    EthereumLabel,
)
from sqlalchemy import text
from sqlalchemy.orm import Session
from web3._utils.validation import validate_abi


from .middleware import MoonstreamHTTPException
from . import data
from .reporter import reporter
from .settings import ETHERSCAN_SMARTCONTRACTS_BUCKET
from bugout.data import BugoutResource
from .settings import (
    MOONSTREAM_APPLICATION_ID,
    bugout_client as bc,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_DATA_JOURNAL_ID,
    AWS_S3_SMARTCONTRACTS_ABI_BUCKET,
    AWS_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from web3 import Web3

logger = logging.getLogger(__name__)


class StatusAPIException(Exception):
    """
    Raised during checking Moonstream API statuses.
    """


class LabelNames(Enum):
    ETHERSCAN_SMARTCONTRACT = "etherscan_smartcontract"
    COINMARKETCAP_TOKEN = "coinmarketcap_token"
    ERC721 = "erc721"


def get_contract_source_info(
    db_session: Session, contract_address: str
) -> Optional[data.EthereumSmartContractSourceInfo]:
    label = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == contract_address)
        .filter(EthereumLabel.label == LabelNames.ETHERSCAN_SMARTCONTRACT.value)
        .one_or_none()
    )
    if label is None:
        return None

    object_uri = label.label_data["object_uri"]
    key = object_uri.split("s3://etherscan-smart-contracts/")[1]
    s3 = boto3.client("s3")
    bucket = ETHERSCAN_SMARTCONTRACTS_BUCKET
    try:
        raw_obj = s3.get_object(Bucket=bucket, Key=key)
        obj_data = json.loads(raw_obj["Body"].read().decode("utf-8"))["data"]
        contract_source_info = data.EthereumSmartContractSourceInfo(
            name=obj_data["ContractName"],
            source_code=obj_data["SourceCode"],
            compiler_version=obj_data["CompilerVersion"],
            abi=obj_data["ABI"],
        )
        return contract_source_info
    except Exception as e:
        logger.error(f"Failed to load smart contract {object_uri}")
        reporter.error_report(e)

    return None


def get_ens_name(web3: Web3, address: str) -> Optional[str]:
    try:
        checksum_address = web3.toChecksumAddress(address)
    except:
        raise ValueError(f"{address} is invalid ethereum address is passed")
    try:
        ens_name = web3.ens.name(checksum_address)
        return ens_name
    except Exception as e:
        reporter.error_report(e, ["web3", "ens"])
        logger.error(
            f"Cannot get ens name for address {checksum_address}. Probably node is down"
        )
        raise e


def get_ens_address(web3: Web3, name: str) -> Optional[str]:

    if not is_valid_ens_name(name):
        raise ValueError(f"{name} is not valid ens name")

    try:
        ens_checksum_address = web3.ens.address(name)
        if ens_checksum_address is not None:
            ordinary_address = ens_checksum_address.lower()
            return ordinary_address
        return None
    except Exception as e:
        reporter.error_report(e, ["web3", "ens"])
        logger.error(f"Cannot get ens address for name {name}. Probably node is down")
        raise e


def get_ethereum_address_info(
    db_session: Session, web3: Web3, address: str
) -> Optional[data.EthereumAddressInfo]:

    if not is_address(address):
        raise ValueError(f"Invalid ethereum address : {address}")

    address_info = data.EthereumAddressInfo(address=address)

    try:
        address_info.ens_name = get_ens_name(web3, address)
    except:
        pass

    etherscan_address_url = f"https://etherscan.io/address/{address}"
    etherscan_token_url = f"https://etherscan.io/token/{address}"
    blockchain_com_url = f"https://www.blockchain.com/eth/address/{address}"

    coinmarketcap_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.COINMARKETCAP_TOKEN.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )

    if coinmarketcap_label is not None:
        address_info.token = data.EthereumTokenDetails(
            name=coinmarketcap_label.label_data["name"],
            symbol=coinmarketcap_label.label_data["symbol"],
            external_url=[
                coinmarketcap_label.label_data["coinmarketcap_url"],
                etherscan_token_url,
                blockchain_com_url,
            ],
        )

    # Checking for smart contract
    etherscan_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.ETHERSCAN_SMARTCONTRACT.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )
    if etherscan_label is not None:
        address_info.smart_contract = data.EthereumSmartContractDetails(
            name=etherscan_label.label_data["name"],
            external_url=[etherscan_address_url, blockchain_com_url],
        )

    # Checking for NFT
    # Checking for smart contract
    erc721_label: Optional[EthereumLabel] = (
        db_session.query(EthereumLabel)
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label == LabelNames.ERC721.value)
        .order_by(text("created_at desc"))
        .limit(1)
        .one_or_none()
    )
    if erc721_label is not None:
        address_info.nft = data.EthereumNFTDetails(
            name=erc721_label.label_data.get("name"),
            symbol=erc721_label.label_data.get("symbol"),
            total_supply=erc721_label.label_data.get("totalSupply"),
            external_url=[etherscan_token_url, blockchain_com_url],
        )
    return address_info


def get_address_labels(
    db_session: Session, start: int, limit: int, addresses: Optional[str] = None
) -> data.AddressListLabelsResponse:
    """
    Attach labels to addresses.
    """
    if addresses is not None:
        addresses_list = addresses.split(",")
        addresses_obj = addresses_list[start : start + limit]
    else:
        addresses_obj = []

    addresses_response = data.AddressListLabelsResponse(addresses=[])

    for address in addresses_obj:
        labels_obj = (
            db_session.query(EthereumLabel)
            .filter(EthereumLabel.address == address)
            .all()
        )
        addresses_response.addresses.append(
            data.AddressLabelsResponse(
                address=address,
                labels=[
                    data.AddressLabelResponse(
                        label=label.label, label_data=label.label_data
                    )
                    for label in labels_obj
                ],
            )
        )

    return addresses_response


def create_onboarding_resource(
    token: uuid.UUID,
    resource_data: Dict[str, Any] = {
        "type": data.USER_ONBOARDING_STATE,
        "steps": {
            "welcome": 0,
            "subscriptions": 0,
            "stream": 0,
        },
        "is_complete": False,
    },
) -> BugoutResource:

    resource = bc.create_resource(
        token=token,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=resource_data,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    return resource


def check_api_status():
    crawl_types_timestamp: Dict[str, Any] = {
        "ethereum_txpool": None,
        "ethereum_trending": None,
    }
    for crawl_type in crawl_types_timestamp.keys():
        try:
            search_results: BugoutSearchResults = bc.search(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=MOONSTREAM_DATA_JOURNAL_ID,
                query=f"tag:crawl_type:{crawl_type}",
                limit=1,
                content=False,
                timeout=10.0,
                order=SearchOrder.DESCENDING,
            )
            if len(search_results.results) == 1:
                crawl_types_timestamp[crawl_type] = search_results.results[0].created_at
        except Exception:
            raise StatusAPIException(
                f"Unable to get status for crawler with type: {crawl_type}"
            )

    return crawl_types_timestamp


def validate_abi_string(abi: str) -> None:
    """
    Transform string to json and run validation
    """

    try:
        validate_abi(json.loads(abi))
    except json.JSONDecodeError:
        raise MoonstreamHTTPException(status_code=400, detail="Malformed abi body.")
    except ValueError as e:
        raise MoonstreamHTTPException(status_code=400, detail=e)
    except:
        raise MoonstreamHTTPException(
            status_code=400, detail="Error on abi valiadation."
        )


def upload_abi_to_s3(
    resource: BugoutResource,
    abi: str,
    update: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Uploading ABI to s3 bucket. Return object for updating resource.

    """

    s3_client = boto3.client("s3")

    bucket = AWS_S3_SMARTCONTRACTS_ABI_BUCKET

    result_bytes = abi.encode("utf-8")
    result_key = f"{AWS_S3_SMARTCONTRACTS_ABI_PREFIX}/{resource.resource_data['address']}/{resource.id}/abi.json"

    s3_client.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"Moonstream": "Abi data"},
    )

    update["abi"] = True

    update["bucket"] = AWS_S3_SMARTCONTRACTS_ABI_BUCKET
    update[
        "s3_path"
    ] = f"{AWS_S3_SMARTCONTRACTS_ABI_PREFIX}/{resource.resource_data['address']}/{resource.id}/abi.json"

    return update
