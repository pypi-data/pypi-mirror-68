import pytest

from mspyteams import Card


@pytest.fixture
def card():
    """Card fixture."""
    return Card()
