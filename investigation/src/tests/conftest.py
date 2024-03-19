import asyncio

import pytest

pytest_plugins = [
    "tests.fixtures.clients",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()