import os
from typing import cast

from bugout.app import Bugout

# Bugout
BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")
bugout_client = Bugout(brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_URL)

HUMBUG_REPORTER_CRAWLERS_TOKEN = os.environ.get("HUMBUG_REPORTER_CRAWLERS_TOKEN")

# Origin
RAW_ORIGINS = os.environ.get("MOONSTREAM_CORS_ALLOWED_ORIGINS")
if RAW_ORIGINS is None:
    raise ValueError(
        "MOONSTREAM_CORS_ALLOWED_ORIGINS environment variable must be set (comma-separated list of CORS allowed origins)"
    )
ORIGINS = RAW_ORIGINS.split(",")

# OpenAPI
DOCS_TARGET_PATH = "docs"

# Geth connection address
MOONSTREAM_NODE_ETHEREUM_IPC_ADDR = os.environ.get(
    "MOONSTREAM_NODE_ETHEREUM_IPC_ADDR", "127.0.0.1"
)
MOONSTREAM_NODE_ETHEREUM_IPC_PORT = os.environ.get(
    "MOONSTREAM_NODE_ETHEREUM_IPC_PORT", 8545
)
MOONSTREAM_ETHEREUM_IPC_PATH = (
    f"http://{MOONSTREAM_NODE_ETHEREUM_IPC_ADDR}:{MOONSTREAM_NODE_ETHEREUM_IPC_PORT}"
)
MOONSTREAM_NODE_POLYGON_IPC_ADDR = os.environ.get(
    "MOONSTREAM_NODE_POLYGON_IPC_ADDR", "127.0.0.1"
)
MOONSTREAM_NODE_POLYGON_IPC_PORT = os.environ.get(
    "MOONSTREAM_NODE_POLYGON_IPC_PORT", 8545
)
MOONSTREAM_POLYGON_IPC_PATH = (
    f"http://{MOONSTREAM_NODE_POLYGON_IPC_ADDR}:{MOONSTREAM_NODE_POLYGON_IPC_PORT}"
)

MOONSTREAM_CRAWL_WORKERS = 4
MOONSTREAM_CRAWL_WORKERS_RAW = os.environ.get("MOONSTREAM_CRAWL_WORKERS")
try:
    if MOONSTREAM_CRAWL_WORKERS_RAW is not None:
        MOONSTREAM_CRAWL_WORKERS = int(MOONSTREAM_CRAWL_WORKERS_RAW)
except:
    raise Exception(
        f"Could not parse MOONSTREAM_CRAWL_WORKERS as int: {MOONSTREAM_CRAWL_WORKERS_RAW}"
    )

# Etherscan
MOONSTREAM_ETHERSCAN_TOKEN = os.environ.get("MOONSTREAM_ETHERSCAN_TOKEN")

# NFT crawler
NFT_HUMBUG_TOKEN = os.environ.get("NFT_HUMBUG_TOKEN", "")
if NFT_HUMBUG_TOKEN == "":
    raise ValueError("NFT_HUMBUG_TOKEN env variable is not set")

MOONSTREAM_ADMIN_ACCESS_TOKEN = os.environ.get("MOONSTREAM_ADMIN_ACCESS_TOKEN", "")
if MOONSTREAM_ADMIN_ACCESS_TOKEN == "":
    raise ValueError("MOONSTREAM_ADMIN_ACCESS_TOKEN env variable is not set")

MOONSTREAM_DATA_JOURNAL_ID = os.environ.get("MOONSTREAM_DATA_JOURNAL_ID", "")
if MOONSTREAM_DATA_JOURNAL_ID == "":
    raise ValueError("MOONSTREAM_DATA_JOURNAL_ID env variable is not set")


MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET environment variable must be set"
    )
MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX = os.environ.get(
    "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX"
)
if MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX is None:
    raise ValueError(
        "MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX environment variable must be set"
    )
