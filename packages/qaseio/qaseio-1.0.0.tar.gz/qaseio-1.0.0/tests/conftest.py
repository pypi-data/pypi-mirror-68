import pytest

from qaseio.client import QaseApi
from qaseio.client.services import BaseService


@pytest.fixture()
def client():
    api = QaseApi("")
    api.projects._in_test = True
    api.test_cases._in_test = True
    api.runs._in_test = True
    api.results._in_test = True
    api.plans._in_test = True
    return api


@pytest.fixture()
def base_service():
    return BaseService(None, None)
