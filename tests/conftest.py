import os
import tempfile

import pytest
from ducks import create_app

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': None,
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

