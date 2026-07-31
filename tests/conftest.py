import pytest
import sys
import os

# Ensure the project root is on sys.path so `import app` works from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app as _app_module


@pytest.fixture()
def client():
    _app_module.app.config['TESTING'] = True
    with _app_module.app.test_client() as c:
        yield c
