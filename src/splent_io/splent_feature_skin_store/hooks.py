"""Storefront header hooks.

The store skin hides the CMS admin toolbar (see skin_store.css) and instead
renders a single minimal auth control at the right end of the public header,
through the ``layout.nav`` hook that ``public_base.html`` already exposes:
"Log in" for anonymous visitors, "Log out" for authenticated users.

SOFT dependency on the auth feature: in a product without auth (no
``auth.login``/``auth.logout`` endpoints or no ``flask_login``) the hook
renders nothing instead of breaking the page.
"""

from flask_babel import gettext as _

from splent_framework.hooks.template_hooks import register_template_hook


def store_auth_link():
    try:
        from flask import url_for
        from flask_login import current_user

        if current_user and getattr(current_user, "is_authenticated", False):
            return (
                f'<a class="store-auth-link" href="{url_for("auth.logout")}">'
                f"{_('Log out')}</a>"
            )
        return (
            f'<a class="store-auth-link" href="{url_for("auth.login")}">'
            f"{_('Log in')}</a>"
        )
    except Exception:
        return ""


register_template_hook("layout.nav", store_auth_link)
