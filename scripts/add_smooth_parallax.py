from pathlib import Path

SCRIPT_MARKER = "/* 313 smooth scroll and parallax */"
CSS_MARKER = "/* 313 smooth scroll and parallax */"

js_path = Path("script.js")
css_path = Path("hero-tilda.css")

js = js_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

js_addition = r'''

/* 313 smooth scroll and parallax */
;(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const smoothEnabled = finePointer && window.innerWidth > 980 && !reducedMotion;
  const root = document.documentElement;
  const heroArt = document.querySelector('.hero-art');
  const parallaxSelector = '.project-media img, .author-photo img, .dialog-gallery figure img';
  const registered = new WeakSet();
  const visibleImages = new Set();
  let parallaxFrame = 0;
  let smoothFrame = 0;
  let smoothRunning = false;
  let currentY = window.scrollY;
  let targetY = window.scrollY;

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const maxScroll = () => Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

  function registerParallaxImages(scope = document) {
    if (reducedMotion) return;
    const images = [];
    if (scope instanceof Element && scope.matches(parallaxSelector)) images.push(scope);
    if (scope.querySelectorAll) images.push(...scope.querySelectorAll(parallaxSelector));
    images.forEach((image) => {
      if (registered.has(image)) return;
      registered.add(image);
      image.setAttribute('data-parallax-image', '');
      parallaxObserver.observe(image);
    });
  }

  function updateParallax() {
    parallaxFrame = 0;
    if (reducedMotion) return;
    const viewportHeight = window.innerHeight || 1;
    const strength = window.innerWidth <= 700 ? 14 : window.innerWidth <= 980 ? 20 : 34;

    visibleImages.forEach((image) => {
      if (!image.isConnected) {
        visibleImages.delete(image);
        return;
      }
      const container = image.closest('.project-media, .author-photo, .dialog-gallery figure');
      if (!container) return;
      const rect = container.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const progress = (center - viewportHeight / 2) / (viewportHeight / 2 + rect.height / 2);
      const offset = clamp(progress, -1, 1) * -strength;
      image.style.setProperty('--parallax-y', `${offset.toFixed(2)}px`);
    });

    if (heroArt) {
      const heroOffset = clamp(window.scrollY * 0.11, 0, window.innerWidth <= 700 ? 34 : 64);
      heroArt.style.setProperty('--hero-parallax', `${heroOffset.toFixed(2)}px`);
    }
  }

  function requestParallax() {
    if (!parallaxFrame) parallaxFrame = requestAnimationFrame(updateParallax);
  }

  const parallaxObserver = reducedMotion || !('IntersectionObserver' in window)
    ? { observe(image) { visibleImages.add(image); requestParallax(); } }
    : new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) visibleImages.add(entry.target);
          else visibleImages.delete(entry.target);
        });
        requestParallax();
      }, { rootMargin: '20% 0px 20% 0px', threshold: 0 });

  registerParallaxImages();

  const mutationObserver = new MutationObserver((records) => {
    records.forEach((record) => record.addedNodes.forEach((node) => {
      if (node instanceof Element) registerParallaxImages(node);
    }));
    requestParallax();
  });
  mutationObserver.observe(document.body, { childList: true, subtree: true });

  function canScrollNatively(target, deltaY) {
    let element = target instanceof Element ? target : null;
    while (element && element !== document.body) {
      const style = getComputedStyle(element);
      const scrollable = /(auto|scroll)/.test(style.overflowY) && element.scrollHeight > element.clientHeight + 1;
      if (scrollable) {
        const canGoUp = deltaY < 0 && element.scrollTop > 0;
        const canGoDown = deltaY > 0 && element.scrollTop + element.clientHeight < element.scrollHeight - 1;
        if (canGoUp || canGoDown) return true;
      }
      element = element.parentElement;
    }
    return false;
  }

  function animateScroll() {
    smoothFrame = 0;
    smoothRunning = true;
    const difference = targetY - currentY;
    currentY += difference * 0.12;

    if (Math.abs(difference) < 0.45) {
      currentY = targetY;
      window.scrollTo(0, currentY);
      smoothRunning = false;
      requestParallax();
      return;
    }

    window.scrollTo(0, currentY);
    requestParallax();
    smoothFrame = requestAnimationFrame(animateScroll);
  }

  function startSmoothScroll() {
    if (!smoothFrame) smoothFrame = requestAnimationFrame(animateScroll);
  }

  function cancelSmoothScroll() {
    if (smoothFrame) cancelAnimationFrame(smoothFrame);
    smoothFrame = 0;
    smoothRunning = false;
    currentY = window.scrollY;
    targetY = window.scrollY;
  }

  if (smoothEnabled) {
    root.classList.add('has-smooth-wheel');

    window.addEventListener('wheel', (event) => {
      if (event.ctrlKey || document.body.classList.contains('dialog-open') || document.body.classList.contains('menu-open')) return;
      if (canScrollNatively(event.target, event.deltaY)) return;
      event.preventDefault();
      const multiplier = event.deltaMode === 1 ? 18 : event.deltaMode === 2 ? window.innerHeight : 1;
      if (!smoothRunning) currentY = window.scrollY;
      targetY = clamp(targetY + event.deltaY * multiplier, 0, maxScroll());
      startSmoothScroll();
    }, { passive: false });

    document.addEventListener('click', (event) => {
      const link = event.target.closest('a[href^="#"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      event.preventDefault();
      const headerHeight = document.querySelector('[data-header]')?.offsetHeight || 0;
      currentY = window.scrollY;
      targetY = clamp(target.getBoundingClientRect().top + window.scrollY - headerHeight - 10, 0, maxScroll());
      startSmoothScroll();
      try { history.pushState(null, '', href); } catch (_) {}
    });

    window.addEventListener('pointerdown', () => {
      if (smoothRunning) cancelSmoothScroll();
    }, { passive: true });

    window.addEventListener('keydown', (event) => {
      if (['PageUp', 'PageDown', 'Home', 'End', 'ArrowUp', 'ArrowDown', ' '].includes(event.key)) cancelSmoothScroll();
    });
  }

  window.addEventListener('scroll', () => {
    if (!smoothRunning) {
      currentY = window.scrollY;
      targetY = window.scrollY;
    }
    requestParallax();
  }, { passive: true });
  window.addEventListener('resize', requestParallax, { passive: true });
  requestParallax();
})();
'''

css_addition = r'''

/* 313 smooth scroll and parallax */
html{scroll-padding-top:88px}
html.has-smooth-wheel{scroll-behavior:auto!important}
.hero-art{transform:translate3d(0,var(--hero-parallax,0px),0) scale(1.045);transform-origin:center top;will-change:transform}
[data-parallax-image]{will-change:transform;backface-visibility:hidden;transform:translate3d(0,var(--parallax-y,0px),0)!important}
.project-media img[data-parallax-image]{height:116%;margin-top:-8%;scale:1.035;transition:scale .75s var(--ease),filter .6s var(--ease)}
.project-button:hover .project-media img[data-parallax-image]{scale:1.09}
.author-photo img[data-parallax-image]{height:112%;margin-top:-6%;scale:1.025;transition:scale .75s var(--ease),filter .6s var(--ease)}
.author-card:hover .author-photo img[data-parallax-image]{scale:1.065}
.dialog-gallery figure img[data-parallax-image]{height:auto!important;margin:0;scale:1.025;transform-origin:center center}
@media(max-width:980px){html{scroll-padding-top:76px}.project-media img[data-parallax-image]{height:112%;margin-top:-6%;scale:1.025}.author-photo img[data-parallax-image]{height:108%;margin-top:-4%}.dialog-gallery figure img[data-parallax-image]{scale:1.015}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.hero-art,[data-parallax-image]{transform:none!important;scale:1!important;margin-top:0!important;height:100%!important;will-change:auto!important}}
'''

if SCRIPT_MARKER not in js:
    js_path.write_text(js.rstrip() + js_addition, encoding="utf-8")
if CSS_MARKER not in css:
    css_path.write_text(css.rstrip() + css_addition, encoding="utf-8")

print("Smooth scrolling and parallax added")
