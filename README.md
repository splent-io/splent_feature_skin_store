# splent_feature_skin_store

Storefront skin for the SPLENT marketplace product: an App Store × PyPI look
built on the splent.io brand (light UI, ink navy headings, brand blue,
sparing amber accents).

A skin in SPLENT is a `light` feature that layers aesthetics on top of the
brand-agnostic theme: it sets the design tokens and registers one stylesheet
that cascades last. All markup lives in the content features (marketplace,
configurator); this feature only styles it.

## What it provides

- `THEME_TOKENS` (`STORE_TOKENS`): the splent.io palette shared with the
  landing page and docs — brand `#1a73b2`, ink `#0a0f1a`, amber `#e9b71f`,
  Inter type.
- `skin_store.css` (asset order 200): storefront chrome — hero, search, cards,
  detail sheet, terminal snippets, configurator states, collapsible SPL rows.
- A minimal auth control in the public header (`layout.nav` hook): "Log in" /
  "Log out", soft against products without the auth feature.
- Suppression of the CMS admin toolbar, which belongs to wp-admin-style
  products and not a public storefront (framework hook-override seam plus a
  CSS belt).

## Usage

Select it in a product derived from `marketplace_spl` (optional feature
`skin_store`), or install it directly:

```bash
splent feature:install splent-io/splent_feature_skin_store
```

## Tests

```bash
splent feature:test skin_store
```
