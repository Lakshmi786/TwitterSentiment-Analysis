import os
import tempfile

import pytest

from app import app


@pytest.fixture
def test_helloworld_page(client):

    resp = client.get('/')
    assert b'Hello world' in resp.data