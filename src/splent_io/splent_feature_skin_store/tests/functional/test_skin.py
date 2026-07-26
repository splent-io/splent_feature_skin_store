"""
Functional tests for splent_feature_skin_store.

They pin the load-bearing work of init_feature — the storefront loses its
whole skin if any of this silently breaks — plus the storefront chrome:
the CMS admin toolbar is hidden and a minimal auth control renders in the
public header.
"""

import re

from splent_io.splent_feature_skin_store import STORE_TOKENS


def _skin_css(test_client):
    """The skin stylesheet as linked by a real public page."""
    response = test_client.get("/", follow_redirects=True)
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    match = re.search(r'href="([^"]*skin_store[^"]*\.css[^"]*)"', html)
    assert match, "public pages must link the skin_store stylesheet"
    asset = test_client.get(match.group(1))
    assert asset.status_code == 200
    return html, asset.data.decode("utf-8")


def test_theme_tokens_are_the_store_tokens(test_client):
    assert test_client.application.config["THEME_TOKENS"] == STORE_TOKENS


def test_public_page_links_the_skin_and_the_asset_is_served(test_client):
    html, css = _skin_css(test_client)
    assert "store-hero" in css  # sanity: it is the storefront stylesheet


def test_skin_hides_the_cms_admin_toolbar(test_client):
    """The admin feature injects a WordPress-style toolbar on every public
    page for authenticated users; the storefront skin suppresses it."""
    _, css = _skin_css(test_client)
    adminbar_rule = css.split("#sp-adminbar")[1].split("}")[0]
    assert "display: none" in adminbar_rule


def test_header_shows_log_in_for_anonymous_visitors(test_client):
    response = test_client.get("/", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert 'class="store-auth-link"' in html
    assert ">Log in</a>" in html
    assert ">Log out</a>" not in html


def test_header_shows_log_out_for_authenticated_users(test_client, monkeypatch):
    import flask_login.utils as flask_login_utils

    class _AuthenticatedUser:
        is_authenticated = True

    monkeypatch.setattr(
        flask_login_utils, "_get_user", lambda: _AuthenticatedUser()
    )
    response = test_client.get("/", follow_redirects=True)
    html = response.data.decode("utf-8")
    assert ">Log out</a>" in html
    assert ">Log in</a>" not in html
    # The CMS admin toolbar is suppressed for authenticated users too:
    # init_feature removes the layout.body_start hook of the admin feature.
    assert "sp-adminbar" not in html
