"""
Unit tests for splent_feature_skin_store.

The skin is a light feature: its real work is done in init_feature (theme
tokens + stylesheet registration, covered by the functional tests) and in the
header auth-control hook. These tests pin the parts that need no app.
"""

from splent_io.splent_feature_skin_store import STORE_TOKENS
from splent_io.splent_feature_skin_store.hooks import store_auth_link

# The token keys public_base.html / the theme CSS variables rely on.
REQUIRED_TOKEN_KEYS = {
    "primary",
    "primary_contrast",
    "accent",
    "bg",
    "surface",
    "text",
    "heading",
    "muted",
    "border",
    "radius",
    "container",
    "font_body",
    "font_heading",
}


def test_store_tokens_cover_the_theme_contract():
    missing = REQUIRED_TOKEN_KEYS - set(STORE_TOKENS)
    assert not missing, f"STORE_TOKENS is missing theme keys: {sorted(missing)}"


def test_store_auth_link_degrades_without_a_request_context():
    """SOFT dependency on auth: outside a request (or in a product without
    auth endpoints) the hook renders nothing instead of raising."""
    assert store_auth_link() == ""
