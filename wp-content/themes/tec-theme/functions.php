<?php
/**
 * TEC Theme bootstrap file.
 */

define('TEC_THEME_VERSION', '0.1.0');

defined('TEC_THEME_PATH') || define('TEC_THEME_PATH', get_template_directory());
defined('TEC_THEME_URI') || define('TEC_THEME_URI', get_template_directory_uri());

require_once TEC_THEME_PATH . '/inc/factions.php';

/**
 * Theme setup hooks.
 */
function tec_theme_setup(): void {
    load_theme_textdomain('tec-theme', TEC_THEME_PATH . '/languages');

    add_theme_support('automatic-feed-links');
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('custom-logo', [
        'height'      => 80,
        'width'       => 80,
        'flex-height' => true,
        'flex-width'  => true,
    ]);

    register_nav_menus([
        'primary'  => __('Primary Menu', 'tec-theme'),
        'footer'   => __('Footer Menu', 'tec-theme'),
        'factions' => __('Factions Menu', 'tec-theme'),
    ]);

    add_theme_support('html5', [
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ]);
}
add_action('after_setup_theme', 'tec_theme_setup');

/**
 * Enqueue front-end assets.
 */
function tec_theme_scripts(): void {
    wp_enqueue_style('tec-theme-style', get_stylesheet_uri(), [], TEC_THEME_VERSION);
    wp_enqueue_style(
        'tec-theme-header',
        TEC_THEME_URI . '/assets/css/header.css',
        ['tec-theme-style'],
        TEC_THEME_VERSION
    );

    wp_enqueue_script(
        'tec-theme-header',
        TEC_THEME_URI . '/assets/js/header.js',
        [],
        TEC_THEME_VERSION,
        true
    );

    $asset   = sanitize_key(get_theme_mod('tec_crypto_asset', 'bitcoin'));
    $currency = sanitize_key(get_theme_mod('tec_crypto_currency', 'usd'));
    $label   = strtoupper(sanitize_text_field(get_theme_mod('tec_crypto_label', 'BTC')));

    wp_localize_script('tec-theme-header', 'tecThemeHeader', [
        'crypto'  => [
            'asset'    => $asset ?: 'bitcoin',
            'currency' => $currency ?: 'usd',
            'label'    => $label ?: 'BTC',
            'endpoint' => 'https://api.coingecko.com/api/v3/simple/price',
        ],
        'strings' => [
            'menu'        => __('Menu', 'tec-theme'),
            'factions'    => __('Factions', 'tec-theme'),
            'priceError'  => __('Price unavailable', 'tec-theme'),
            'loadingPrice'=> __('Loading…', 'tec-theme'),
        ],
    ]);
}
add_action('wp_enqueue_scripts', 'tec_theme_scripts');

/**
 * Header controls in Customizer.
 */
function tec_theme_customize_register($wp_customize): void {
    $wp_customize->add_section('tec_theme_header', [
        'title'    => __('Header Settings', 'tec-theme'),
        'priority' => 30,
    ]);

    $wp_customize->add_setting('tec_crypto_asset', [
        'default'           => 'bitcoin',
        'sanitize_callback' => 'sanitize_text_field',
    ]);
    $wp_customize->add_control('tec_crypto_asset', [
        'label'   => __('Crypto Asset (CoinGecko ID)', 'tec-theme'),
        'section' => 'tec_theme_header',
        'type'    => 'text',
    ]);

    $wp_customize->add_setting('tec_crypto_currency', [
        'default'           => 'usd',
        'sanitize_callback' => 'sanitize_text_field',
    ]);
    $wp_customize->add_control('tec_crypto_currency', [
        'label'   => __('Fiat Currency Code', 'tec-theme'),
        'section' => 'tec_theme_header',
        'type'    => 'text',
    ]);

    $wp_customize->add_setting('tec_crypto_label', [
        'default'           => 'BTC',
        'sanitize_callback' => 'sanitize_text_field',
    ]);
    $wp_customize->add_control('tec_crypto_label', [
        'label'       => __('Ticker Label', 'tec-theme'),
        'section'     => 'tec_theme_header',
        'type'        => 'text',
        'description' => __('Displayed label in the header.', 'tec-theme'),
    ]);
}
add_action('customize_register', 'tec_theme_customize_register');
