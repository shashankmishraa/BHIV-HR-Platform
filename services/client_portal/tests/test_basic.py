"""Basic tests for Client Portal service."""

import pytest


def test_import():
    """Test basic import."""
    from services.client_portal import app

    assert app is not None
