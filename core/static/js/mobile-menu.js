/* -------------------------------------------------
   Mobile menu toggle
   ------------------------------------------------- */
const menuBtn   = document.getElementById('menu-toggle');
const mobileNav = document.getElementById('mobile-nav');

menuBtn?.addEventListener('click', () => {
    mobileNav?.classList.toggle('hidden');
});

const revealObserver = new IntersectionObserver(
    entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.1 }
);

document.querySelectorAll('.slide-in-left,.slide-in-right,.slide-in-up,.feature-card')
        .forEach(el => revealObserver.observe(el));


const heroSection = document.querySelector('section.hero');
const stickyCTA    = document.getElementById('sticky-cta');

if (heroSection && stickyCTA) {
    const heroObs = new IntersectionObserver(
        ([e]) => stickyCTA.classList.toggle('hidden', e.isIntersecting),
        { rootMargin: '-80px 0px 0px 0px' }
    );
    heroObs.observe(heroSection);
}