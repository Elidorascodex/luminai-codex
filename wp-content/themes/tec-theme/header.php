<!doctype html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <?php wp_head(); ?>
</head>

<body <?php body_class('no-js'); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
    <a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e('Skip to content', 'tec-theme'); ?></a>

    <header id="masthead" class="site-header">
        <div class="header-container">
            <div class="site-branding">
                <?php
                if (function_exists('the_custom_logo') && has_custom_logo()) {
                    the_custom_logo();
                } else {
                    printf(
                        '<a class="site-title" href="%1$s">%2$s</a>',
                        esc_url(home_url('/')),
                        esc_html(get_bloginfo('name'))
                    );
                }
                ?>
            </div>

            <button class="menu-toggle" aria-controls="primary-menu-container" aria-expanded="false">
                <span class="menu-toggle-bars" aria-hidden="true">
                    <span class="menu-toggle-bar"></span>
                    <span class="menu-toggle-bar"></span>
                    <span class="menu-toggle-bar"></span>
                </span>
                <span class="menu-toggle-label"><?php esc_html_e('Menu', 'tec-theme'); ?></span>
            </button>

            <nav id="site-navigation" class="main-navigation" aria-label="<?php esc_attr_e('Primary Menu', 'tec-theme'); ?>">
                <div class="primary-menu-container" id="primary-menu-container">
                    <?php
                    wp_nav_menu([
                        'theme_location' => 'primary',
                        'menu_id'        => 'primary-menu',
                        'menu_class'     => 'primary-menu',
                        'container'      => false,
                        'fallback_cb'    => 'wp_page_menu',
                    ]);
                    ?>
                </div>
            </nav>

            <div class="header-factions">
                <button class="factions-toggle" aria-controls="factions-menu" aria-expanded="false">
                    <span class="faction-icon-placeholder" aria-hidden="true">F</span>
                    <span><?php esc_html_e('Factions', 'tec-theme'); ?></span>
                    <span class="dropdown-caret" aria-hidden="true">▼</span>
                </button>
                <div class="factions-dropdown" aria-hidden="true">
                    <nav class="factions-navigation" aria-label="<?php esc_attr_e('Faction Menu', 'tec-theme'); ?>">
                        <?php
                        wp_nav_menu([
                            'theme_location' => 'factions',
                            'menu_id'        => 'factions-menu',
                            'menu_class'     => 'factions-menu-container',
                            'container'      => false,
                            'fallback_cb'    => 'tec_theme_factions_fallback',
                        ]);
                        ?>
                    </nav>
                </div>
            </div>

            <?php
            $crypto_asset   = sanitize_key(get_theme_mod('tec_crypto_asset', 'bitcoin'));
            $crypto_currency = sanitize_key(get_theme_mod('tec_crypto_currency', 'usd'));
            $crypto_label   = strtoupper(sanitize_text_field(get_theme_mod('tec_crypto_label', 'BTC')));
            ?>
            <div class="header-crypto-tracker">
                <button class="crypto-tracker-toggle" data-crypto-asset="<?php echo esc_attr($crypto_asset); ?>" data-crypto-currency="<?php echo esc_attr($crypto_currency); ?>" aria-live="polite">
                    <span class="crypto-icon-placeholder" aria-hidden="true">C</span>
                    <span class="crypto-label"><?php echo esc_html($crypto_label); ?></span>
                    <span class="crypto-price">
                        <span class="tec-price-value" data-loading-text="<?php esc_attr_e('Loading…', 'tec-theme'); ?>">$---.--</span>
                    </span>
                </button>
            </div>
        </div>
    </header>

    <div id="primary" class="site-content">
