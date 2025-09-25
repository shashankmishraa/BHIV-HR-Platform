"""
Centralized static assets management
"""

import os


def get_favicon_path():
    """Get path to centralized favicon"""
    return os.path.join(os.path.dirname(__file__), "..", "..", "static", "favicon.ico")


def get_static_asset_url(asset_name: str, base_url: str = ""):
    """Get URL for static assets"""
    return f"{base_url}/static/{asset_name}"
