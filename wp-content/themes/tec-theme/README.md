# TEC Theme Header

A minimal WordPress theme that implements the TEC header experience featuring:

- Sticky global header with custom logo/site title
- Responsive primary navigation with accessible menu toggle
- Factions dropdown with JSON-powered fallback
- Crypto tracker button that fetches live prices from CoinGecko

## Getting Started

1. Copy the `tec-theme` directory into `wp-content/themes/` in your WordPress install.
2. Activate "TEC Theme" under **Appearance → Themes**.
3. Assign menus for **Primary**, **Factions**, and **Footer** under **Appearance → Menus**.
4. Optional: Adjust the crypto tracker asset/currency/label under **Appearance → Customize → Header Settings**.

Faction data for the fallback dropdown lives in `assets/data/factions.json`. Update this file or register a `factions` menu for full control from the WordPress admin.
