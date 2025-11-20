<?php
/**
 * Helpers for faction data/menus.
 */

if (!function_exists('tec_get_factions_data')) {
    function tec_get_factions_data(): array {
        $cached = get_transient('tec_factions_data');
        if ($cached !== false) {
            return $cached;
        }

        $json_path = TEC_THEME_PATH . '/assets/data/factions.json';
        if (!file_exists($json_path)) {
            return ['error' => __('Faction data file not found.', 'tec-theme')];
        }

        $contents = file_get_contents($json_path);
        if ($contents === false) {
            return ['error' => __('Unable to read faction data.', 'tec-theme')];
        }

        $decoded = json_decode($contents, true);
        if (!is_array($decoded)) {
            return ['error' => __('Faction data is invalid JSON.', 'tec-theme')];
        }

        set_transient('tec_factions_data', $decoded, HOUR_IN_SECONDS);
        return $decoded;
    }
}

if (!function_exists('tec_theme_factions_fallback')) {
    function tec_theme_factions_fallback(): void {
        $factions_data = tec_get_factions_data();
        if (isset($factions_data['error'])) {
            echo '<ul id="factions-menu" class="factions-menu-container">';
            echo '<li class="menu-item"><a href="#">' . esc_html($factions_data['error']) . '</a></li>';
            echo '</ul>';
            return;
        }

        if (empty($factions_data['factions'])) {
            echo '<ul id="factions-menu" class="factions-menu-container">';
            echo '<li class="menu-item"><a href="#">' . esc_html__('No Factions Found', 'tec-theme') . '</a></li>';
            echo '</ul>';
            return;
        }

        echo '<ul id="factions-menu" class="factions-menu-container">';
        foreach ($factions_data['factions'] as $faction) {
            if (empty($faction['name'])) {
                continue;
            }
            $name  = $faction['name'];
            $slug  = isset($faction['slug']) ? $faction['slug'] : sanitize_title($name);
            $url   = isset($faction['url']) ? $faction['url'] : home_url('/faction/' . $slug);
            $class = 'menu-item faction-item faction-' . esc_attr($slug);
            echo '<li class="' . $class . '">';
            echo '<a href="' . esc_url($url) . '">' . esc_html($name) . '</a>';
            if (!empty($faction['tagline'])) {
                echo '<span class="faction-tagline">' . esc_html($faction['tagline']) . '</span>';
            }
            echo '</li>';
        }
        echo '</ul>';
    }
}

add_action('switch_theme', 'tec_theme_clear_factions_cache');
add_action('customize_save_after', 'tec_theme_clear_factions_cache');

function tec_theme_clear_factions_cache(): void {
    delete_transient('tec_factions_data');
}
