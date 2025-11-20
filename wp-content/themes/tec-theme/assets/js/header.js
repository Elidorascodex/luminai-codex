(function () {
    const doc = document;
    doc.documentElement.classList.add('js-enabled');
    if (doc.body) {
        doc.body.classList.remove('no-js');
    }

    const navToggle = doc.querySelector('.menu-toggle');
    const navContainer = doc.getElementById('primary-menu-container');
    const factionWrapper = doc.querySelector('.header-factions');
    const factionToggle = doc.querySelector('.factions-toggle');
    const factionDropdown = doc.querySelector('.factions-dropdown');
    const cryptoButton = doc.querySelector('.crypto-tracker-toggle');
    const priceElement = doc.querySelector('.tec-price-value');

    function closeNav() {
        if (!navToggle || !navContainer) return;
        navContainer.classList.remove('is-open');
        navToggle.classList.remove('is-active');
        navToggle.setAttribute('aria-expanded', 'false');
    }

    if (navToggle && navContainer) {
        navToggle.addEventListener('click', () => {
            const isOpen = !navContainer.classList.contains('is-open');
            navContainer.classList.toggle('is-open', isOpen);
            navToggle.classList.toggle('is-active', isOpen);
            navToggle.setAttribute('aria-expanded', String(isOpen));
        });

        doc.addEventListener('click', (event) => {
            if (!navContainer.classList.contains('is-open')) return;
            if (event.target === navToggle || navToggle.contains(event.target)) return;
            if (event.target === navContainer || navContainer.contains(event.target)) return;
            closeNav();
        });

        doc.addEventListener('keyup', (event) => {
            if (event.key === 'Escape') {
                closeNav();
            }
        });
    }

    function closeFactions() {
        if (!factionWrapper || !factionDropdown || !factionToggle) return;
        factionWrapper.classList.remove('is-open');
        factionDropdown.classList.remove('is-open');
        factionDropdown.setAttribute('aria-hidden', 'true');
        factionToggle.setAttribute('aria-expanded', 'false');
    }

    if (factionWrapper && factionToggle && factionDropdown) {
        factionToggle.addEventListener('click', () => {
            const isOpen = !factionWrapper.classList.contains('is-open');
            factionWrapper.classList.toggle('is-open', isOpen);
            factionDropdown.classList.toggle('is-open', isOpen);
            factionDropdown.setAttribute('aria-hidden', String(!isOpen));
            factionToggle.setAttribute('aria-expanded', String(isOpen));
        });

        doc.addEventListener('click', (event) => {
            if (!factionWrapper.classList.contains('is-open')) return;
            if (factionWrapper.contains(event.target)) return;
            closeFactions();
        });

        doc.addEventListener('keyup', (event) => {
            if (event.key === 'Escape') {
                closeFactions();
            }
        });
    }

    function formatCurrency(value, currency) {
        try {
            return new Intl.NumberFormat(undefined, {
                style: 'currency',
                currency: currency.toUpperCase(),
                minimumFractionDigits: 2,
            }).format(value);
        } catch (error) {
            return `$${Number(value).toFixed(2)}`;
        }
    }

    function fetchCryptoPrice() {
        if (!priceElement || !cryptoButton || typeof fetch === 'undefined') {
            return;
        }

        const localized = (typeof window !== 'undefined' && window.tecThemeHeader) ? window.tecThemeHeader : {};
        const crypto = localized.crypto || {};
        const strings = localized.strings || {};
        const asset = cryptoButton.dataset.cryptoAsset || crypto.asset || 'bitcoin';
        const currency = cryptoButton.dataset.cryptoCurrency || crypto.currency || 'usd';
        const endpoint = crypto.endpoint || 'https://api.coingecko.com/api/v3/simple/price';

        priceElement.classList.add('is-loading');
        priceElement.textContent = priceElement.dataset.loadingText || strings.loadingPrice || 'Loading…';

        const url = `${endpoint}?ids=${encodeURIComponent(asset)}&vs_currencies=${encodeURIComponent(currency)}`;
        fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((json) => {
                const value = json?.[asset]?.[currency];
                if (typeof value === 'number') {
                    priceElement.textContent = formatCurrency(value, currency);
                } else {
                    priceElement.textContent = strings.priceError || 'Price unavailable';
                }
            })
            .catch(() => {
                priceElement.textContent = strings.priceError || 'Price unavailable';
            })
            .finally(() => {
                priceElement.classList.remove('is-loading');
            });
    }

    if (cryptoButton && priceElement) {
        fetchCryptoPrice();
        setInterval(fetchCryptoPrice, 60000);
    }
})();
