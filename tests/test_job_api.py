import pytest


def test_connect(hh_api):
    """Тест метода connect"""
    try:
        hh_api.connect()
    except Exception:
        pytest.fail("connect raised Exception unexpectedly!")
