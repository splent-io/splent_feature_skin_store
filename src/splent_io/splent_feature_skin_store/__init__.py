from splent_framework.blueprints.base_blueprint import create_blueprint

skin_store_bp = create_blueprint(__name__)

# Design tokens — the splent.io brand (ink navy + brand blue + amber accents).
# General UI is LIGHT and clean (docs.splent.io); dark ink surfaces are used
# for hero/terminal blocks inside skin_store.css, not as global tokens.
STORE_TOKENS = {
    "primary": "#1a73b2",  # brand-500
    "primary_contrast": "#ffffff",
    "accent": "#e9b71f",  # amber-550 (sparing accent)
    "bg": "#ffffff",
    "surface": "#f7f9fc",
    "text": "#2a3448",  # ink-500
    "heading": "#0a0f1a",  # ink-900
    "muted": "#61708a",
    "border": "#e3e9f1",
    "radius": "10px",
    "container": "1180px",
    "font_body": "'Inter', system-ui, sans-serif",
    "font_heading": "'Inter', system-ui, sans-serif",
    "font_display": "'Inter', system-ui, sans-serif",
    "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
}


def init_feature(app):
    # A skin sets the theme tokens and registers its stylesheet (order 200, so
    # it cascades last) on top of the theme's brand-agnostic base public.css.
    from splent_framework.assets.asset_registry import register_asset

    from splent_io.splent_feature_skin_store.config import inject_config

    inject_config(app)
    app.config["THEME_TOKENS"] = STORE_TOKENS
    register_asset(
        "css",
        "skin_store.assets",
        order=200,
        subfolder="css",
        filename="skin_store.css",
    )

    # The CMS admin toolbar (admin feature, layout.body_start hook) does not
    # belong in a public storefront: suppress it through the framework's
    # hook-override seam (skin_store.css also hides #sp-adminbar as a belt).
    # The header keeps a minimal Log in / Log out control instead (hooks.py).
    # SOFT dependency: the admin feature is looked up by module name (like a
    # service_proxy lookup, never a static import), so products without it
    # simply have nothing to remove.
    try:
        import importlib

        from splent_framework.hooks.template_hooks import remove_template_hook

        admin_hooks = importlib.import_module("splent_io.splent_feature_admin.hooks")
        remove_template_hook("layout.body_start", admin_hooks.admin_bar)
    except Exception:
        pass


def inject_context_vars(app):
    return {}
