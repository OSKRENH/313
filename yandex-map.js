(() => {
  const container = document.querySelector('[data-yandex-map]');
  if (!container) return;

  const section = container.closest('.project-map');
  const fallback = section?.querySelector('[data-map-fallback]');
  const panel = section?.querySelector('[data-map-projects-panel]');
  const panelTitle = section?.querySelector('[data-map-city-title]');
  const panelCount = section?.querySelector('[data-map-city-count]');
  const projectList = section?.querySelector('[data-map-project-list]');
  const panelClose = section?.querySelector('[data-map-panel-close]');
  const cityButtons = Array.from(section?.querySelectorAll('[data-map-city]') || []);

  let started = false;
  let mapInstance = null;

  const cities = [
    {
      id: 'moscow', title: 'Москва', coordinates: [55.7558, 37.6173], side: 'right', offset: [-10, -10],
      projects: [{ index: 6, title: 'Летнее кафе' }]
    },
    {
      id: 'ekaterinburg', title: 'Екатеринбург', coordinates: [56.8389, 60.6057], side: 'right-up', offset: [-10, -10],
      projects: [{ index: 4, title: 'Книжный магазин и кофейня' }]
    },
    {
      id: 'chelyabinsk', title: 'Челябинск', coordinates: [55.1644, 61.4368], side: 'right-down', offset: [-10, -10],
      projects: [
        { index: 2, title: 'Баня' },
        { index: 3, title: 'Квартира на Лесопарковой' },
        { index: 7, title: 'Апартаменты' },
        { index: 10, title: 'Свадебный шоурум' },
        { index: 11, title: 'Home Sweet Home' },
        { index: 12, title: 'Квартира — проект 1' },
        { index: 13, title: 'Квартира — проект 2' }
      ]
    },
    {
      id: 'miass', title: 'Миасс', coordinates: [55.0450, 60.1083], side: 'left-down', offset: [-10, -10],
      projects: [{ index: 0, title: 'Квартира Хюгге' }]
    },
    {
      id: 'uvildy', title: 'Увильды', coordinates: [55.5260, 60.5050], side: 'left-up', offset: [-10, -10],
      projects: [{ index: 1, title: 'Салон красоты' }]
    },
    {
      id: 'chelyabinsk-region', title: 'Челябинская область', coordinates: [54.7400, 61.2000], side: 'right-down-far', offset: [-10, -10],
      projects: [{ index: 5, title: 'Салон массажа и медитации' }]
    },
    {
      id: 'massandra', title: 'Массандра', coordinates: [44.5090, 34.1880], side: 'right', offset: [-10, -10],
      projects: [{ index: 8, title: 'Эстетическая косметология' }]
    },
    {
      id: 'tel-aviv', title: 'Тель-Авив', coordinates: [32.0853, 34.7818], side: 'right', offset: [-10, -10],
      projects: [{ index: 9, title: 'Загородный дом' }]
    }
  ];

  function projectWord(count) {
    if (count === 1) return '1 проект';
    if (count >= 2 && count <= 4) return `${count} проекта`;
    return `${count} проектов`;
  }

  function setActiveCity(cityId) {
    cityButtons.forEach((button) => {
      const active = button.dataset.mapCity === cityId;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }

  function closeProjectPanel() {
    if (panel) panel.hidden = true;
    setActiveCity('');
  }

  function goToProject(index) {
    window.dispatchEvent(new CustomEvent('313:project-select', { detail: { index } }));
  }

  function showCity(cityId, options = {}) {
    const city = cities.find((item) => item.id === cityId);
    if (!city || !panel || !panelTitle || !panelCount || !projectList) return;

    panelTitle.textContent = city.title;
    panelCount.textContent = projectWord(city.projects.length);
    projectList.replaceChildren();

    city.projects.forEach((project, order) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'project-map__project';
      button.dataset.projectIndex = String(project.index);
      button.innerHTML = `
        <span class="project-map__project-index">${String(order + 1).padStart(2, '0')}</span>
        <span class="project-map__project-title"></span>
        <span class="project-map__project-arrow" aria-hidden="true">↗</span>
      `;
      button.querySelector('.project-map__project-title').textContent = project.title;
      button.setAttribute('aria-label', `Перейти к проекту «${project.title}»`);
      button.addEventListener('click', () => goToProject(project.index));
      projectList.append(button);
    });

    panel.hidden = false;
    setActiveCity(city.id);

    if (mapInstance && options.centerMap !== false) {
      mapInstance.panTo(city.coordinates, { duration: 350, flying: true });
    }

    if (window.innerWidth < 700 && options.scrollOnMobile !== false) {
      window.requestAnimationFrame(() => panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }));
    }
  }

  cityButtons.forEach((button) => {
    button.setAttribute('aria-pressed', 'false');
    button.addEventListener('click', () => showCity(button.dataset.mapCity, { scrollOnMobile: true }));
  });

  panelClose?.addEventListener('click', closeProjectPanel);
  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && panel && !panel.hidden) closeProjectPanel();
  });

  function showFallback() {
    container.hidden = true;
    if (!fallback) return;

    fallback.hidden = false;
    fallback.style.display = 'block';
    fallback.innerHTML = `
      <iframe
        title="Яндекс.Карта географии проектов студии 313"
        src="https://yandex.ru/map-widget/v1/?ll=47.500000%2C51.500000&z=3"
        loading="lazy"
        referrerpolicy="no-referrer-when-downgrade"
        style="position:absolute;inset:0;width:100%;height:100%;border:0;filter:grayscale(1) sepia(.48) hue-rotate(104deg) saturate(.82) brightness(.62) contrast(1.14);"
      ></iframe>
      <a
        href="https://yandex.ru/maps/?ll=47.500000%2C51.500000&z=3"
        target="_blank"
        rel="noreferrer"
        style="position:absolute;right:18px;bottom:18px;padding:12px 16px;background:rgba(21,54,61,.92);border:1px solid rgba(184,215,207,.4);color:#eef0e8;"
      >Открыть в Яндекс.Картах ↗</a>
    `;
  }

  function initMap() {
    if (!window.ymaps) {
      showFallback();
      return;
    }

    window.ymaps.ready(() => {
      try {
        const map = new window.ymaps.Map(container, {
          center: [51.5, 47.5],
          zoom: 3,
          controls: ['zoomControl']
        }, {
          suppressMapOpenBlock: true,
          yandexMapDisablePoiInteractivity: true,
          minZoom: 2,
          maxZoom: 12
        });
        mapInstance = map;
        map.behaviors.disable('scrollZoom');

        const markerLayout = window.ymaps.templateLayoutFactory.createClass(
          '<div class="ya-project-marker ya-project-marker--$[properties.side]">' +
            '<span class="ya-project-marker__pulse"></span>' +
            '<span class="ya-project-marker__dot"></span>' +
            '<span class="ya-project-marker__label">' +
              '<strong>$[properties.title]</strong>' +
              '<small>$[properties.count]</small>' +
            '</span>' +
          '</div>'
        );

        const collection = new window.ymaps.GeoObjectCollection();
        cities.forEach((city) => {
          const placemark = new window.ymaps.Placemark(city.coordinates, {
            title: city.title,
            count: projectWord(city.projects.length),
            side: city.side
          }, {
            iconLayout: markerLayout,
            iconOffset: city.offset,
            iconShape: {
              type: 'Rectangle',
              coordinates: [[-140, -60], [190, 80]]
            },
            hideIconOnBalloonOpen: false
          });

          placemark.events.add('click', () => showCity(city.id, { scrollOnMobile: true }));
          collection.add(placemark);
        });

        map.geoObjects.add(collection);
        map.setBounds(collection.getBounds(), {
          checkZoomRange: true,
          zoomMargin: window.innerWidth < 700 ? [70, 28, 70, 28] : [90, 130, 90, 130]
        });

        container.classList.add('is-ready');
        window.addEventListener('resize', () => map.container.fitToViewport(), { passive: true });
      } catch (error) {
        console.error('Yandex map initialization failed', error);
        showFallback();
      }
    });
  }

  function loadMap() {
    if (started) return;
    started = true;

    if (window.ymaps) {
      initMap();
      return;
    }

    const key = container.dataset.apiKey?.trim();
    const script = document.createElement('script');
    script.src = `https://api-maps.yandex.ru/2.1/?lang=ru_RU${key ? `&apikey=${encodeURIComponent(key)}` : ''}`;
    script.async = true;
    script.onload = initMap;
    script.onerror = showFallback;
    document.head.append(script);

    window.setTimeout(() => {
      if (!container.classList.contains('is-ready')) showFallback();
    }, 12000);
  }

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      observer.disconnect();
      loadMap();
    }, { rootMargin: '700px 0px' });
    observer.observe(section || container);
  } else {
    loadMap();
  }
})();
