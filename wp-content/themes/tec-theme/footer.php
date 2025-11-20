    </div><!-- #primary -->

    <footer id="colophon" class="site-footer">
        <div class="footer-container">
            <?php
            wp_nav_menu([
                'theme_location' => 'footer',
                'menu_id'        => 'footer-menu',
                'menu_class'     => 'footer-menu',
                'container'      => false,
                'fallback_cb'    => false,
            ]);
            ?>
            <p class="site-info">&copy; <?php echo esc_html(date_i18n('Y')); ?> <?php bloginfo('name'); ?></p>
        </div>
    </footer>
</div><!-- #page -->

<?php wp_footer(); ?>
</body>
</html>
