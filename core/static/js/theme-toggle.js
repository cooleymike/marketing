/* -------------------------------------------------
   Theme toggle – one‑liner, no extra listeners needed
   ------------------------------------------------- */
(() => {
    const toggleBtn = document.getElementById('theme-toggle');
    const iconEl   = document.getElementById('theme-icon');

    const moonSVG = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                     d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>`;
    const sunSVG  = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                     d="M12 3v1m0 16v1m8.66-12.34l-.71.71M4.05 19.95l-.71-.71M21 12h-1M4 12H3
                        m16.95 4.95l-.71-.71M4.05 4.05l-.71.71M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>`;

    const applyTheme = () => {
        const isDark = localStorage.getItem('theme') === 'dark';
        document.documentElement.classList.toggle('dark', isDark);
        iconEl.innerHTML = isDark ? sunSVG : moonSVG;
    };

    toggleBtn.addEventListener('click', () => {
        const nowDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', nowDark ? 'dark' : 'light');
        iconEl.innerHTML = nowDark ? sunSVG : moonSVG;
    });

    applyTheme();
})();