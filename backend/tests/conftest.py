import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["POSTGRES_USER"] = "test"
    os.environ["POSTGRES_PASSWORD"] = "test"
    os.environ["POSTGRES_SERVER"] = "localhost"
    os.environ["POSTGRES_DB"] = "test_db"
    os.environ["ZOHO_BOOKS_AUTHTOKEN"] = "test_token"
    os.environ["ZOHO_ORG_ID"] = "test_org"
    os.environ["POLYGON_RPC_URL"] = "http://localhost:8545"
    os.environ["PRIVATE_KEY"] = "0x0000000000000000000000000000000000000000000000000000000000000000"
    os.environ["CONTRACT_ADDRESS"] = "0x0000000000000000000000000000000000000000"
