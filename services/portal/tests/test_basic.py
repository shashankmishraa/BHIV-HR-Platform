"""Basic tests for Portal service."""

import pytest


def test_import():
    """Test basic import."""
    from services.portal import app

    assert app is not None
