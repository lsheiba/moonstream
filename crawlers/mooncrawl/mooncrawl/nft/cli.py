"""
A command line tool to crawl information about NFTs from various sources.
"""
import argparse
import json
import os
import sys
from typing import cast

from web3 import Web3

from ..ethereum import connect
from .ethereum import summary as ethereum_summary
from ..publish import publish_json
from ..settings import MOONSTREAM_IPC_PATH
from ..version import MOONCRAWL_VERSION


def web3_client_from_cli_or_env(args: argparse.Namespace) -> Web3:
    """
    Returns a web3 client either by parsing "--web3" argument on the given arguments or by looking up
    the MOONSTREAM_IPC_PATH environment variable.
    """
    web3_connection_string = MOONSTREAM_IPC_PATH
    args_web3 = vars(args).get("web3")
    if args_web3 is not None:
        web3_connection_string = cast(str, args_web3)
    if web3_connection_string is None:
        raise ValueError(
            "Could not find Web3 connection information in arguments or in MOONSTREAM_IPC_PATH environment variable"
        )
    return connect(web3_connection_string)


def ethereum_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)
    result = ethereum_summary(web3_client, args.start, args.end, args.address)

    humbug_token = args.humbug
    if humbug_token is None:
        humbug_token = os.environ.get("MOONSTREAM_HUMBUG_TOKEN")
    if humbug_token:
        title = f"NFT activity on the Ethereum blockchain: Blocks {args.start} to {args.end}"
        publish_json(
            "nft_ethereum",
            humbug_token,
            title,
            result,
            tags=[f"crawler_version:{MOONCRAWL_VERSION}"],
            wait=False,
        )
    with args.outfile as ofp:
        json.dump(result, ofp)


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream NFT crawlers")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Subcommands")

    parser_ethereum = subcommands.add_parser(
        "ethereum",
        description="Collect information about NFTs from Ethereum blockchains",
    )
    parser_ethereum.add_argument(
        "-s",
        "--start",
        type=int,
        default=None,
        help="Starting block number (inclusive if block available)",
    )
    parser_ethereum.add_argument(
        "-e",
        "--end",
        type=int,
        default=None,
        help="Ending block number (inclusive if block available)",
    )
    parser_ethereum.add_argument(
        "-a",
        "--address",
        type=str,
        default=None,
        help="(Optional) NFT contract address that you want to limit the crawl to, e.g. 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d for CryptoKitties.",
    )
    parser_ethereum.add_argument(
        "--web3",
        type=str,
        default=None,
        help="(Optional) Web3 connection string. If not provided, uses the value specified by MOONSTREAM_IPC_PATH environment variable.",
    )
    parser_ethereum.add_argument(
        "--humbug",
        default=None,
        help=(
            "If you would like to write this data to a Moonstream journal, please provide a Humbug "
            "token for that here. (This argument overrides any value set in the "
            "MOONSTREAM_HUMBUG_TOKEN environment variable)"
        ),
    )
    parser_ethereum.add_argument(
        "-o",
        "--outfile",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Optional file to write output to. By default, prints to stdout.",
    )

    parser_ethereum.set_defaults(func=ethereum_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
