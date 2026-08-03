(() => {
  const grid = document.querySelector('[data-project-grid]');
  if (!grid) return;

  let highlightTimer = 0;

  function getCards() {
    return Array.from(grid.querySelectorAll('.project-card'));
  }

  function decorateCards() {
    getCards().forEach((card, index) => {
      card.id = `project-${index + 1}`;
      card.dataset.projectIndex = String(index);
    });
  }

  function ensureProjectRendered(index) {
    let attempts = 0;
    decorateCards();

    while (getCards().length <= index && attempts < 10) {
      const before = getCards().length;
      if (typeof window.loadNextBatch === 'function') {
        window.loadNextBatch();
      } else if (typeof loadNextBatch === 'function') {
        loadNextBatch();
      } else {
        break;
      }
      decorateCards();
      attempts += 1;
      if (getCards().length === before) break;
    }

    return getCards()[index] || null;
  }

  function goToProject(index) {
    const card = ensureProjectRendered(index);
    if (!card) return;

    window.clearTimeout(highlightTimer);
    document.querySelectorAll('.project-card.is-map-target').forEach((item) => item.classList.remove('is-map-target'));
    card.classList.add('is-visible', 'is-map-target');

    const header = document.querySelector('[data-header]');
    const offset = (header?.getBoundingClientRect().height || 76) + 24;
    const targetTop = Math.max(0, card.getBoundingClientRect().top + window.scrollY - offset);

    window.history.replaceState(null, '', `#${card.id}`);
    window.scrollTo({ top: targetTop, behavior: 'smooth' });

    window.setTimeout(() => {
      card.querySelector('.project-button')?.focus({ preventScroll: true });
    }, 650);

    highlightTimer = window.setTimeout(() => card.classList.remove('is-map-target'), 2600);
  }

  const observer = new MutationObserver(decorateCards);
  observer.observe(grid, { childList: true });
  decorateCards();

  window.addEventListener('313:project-select', (event) => {
    const index = Number(event.detail?.index);
    if (!Number.isInteger(index) || index < 0) return;
    goToProject(index);
  });
})();
