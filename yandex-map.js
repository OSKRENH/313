(() => {
  const container = document.querySelector('[data-yandex-map]');
  if (!container) return;

  const section = container.closest('.project-map');
  const fallback = section?.querySelector('[data-map-fallback]');
  let started = false;

  const projects = [
    { title: 'Москва', count: '1 проект', coordinates: [55.7558, 37.6173], side: 'right', offset: [-10, -10] },
    { title: 'Екатеринбург', count: '1 проект', coordinates: [56.8389, 60.6057], side: 'right-up', offset: [-10, -10] },
    { title: 'Челябинск', count: '7 проектов', coordinates: [55.1644, 61.4368], side: 'right-down', offset: [-10, -10] },
    { title: 'Миасс', count: '1 проект', coordinates: [55.0450, 60.1083], side: 'left-down', offset: [-10, -10] },
    { title: 'Увильды', count: '1 проект', coordinates: [55.5260, 60.5050], side: 'left-up', offset: [-10, -10] },
    { title: 'Челябинская область', count: '1 проект', coordinates: [54.7400, 61.2000], side: 'right-down-far', offset: [-10, -10] },
    { title: 'Массандра', count: '1 проект', coordinates: [44.5090, 34.1880], side: 'right', offset: [-10, -10] },
    { title: 'Тель-Авив', count: '1 проект', coordinates: [32.0853, 34.7818], side: 'right', offset: [-10, -10] }
  ];

  function showFallback() {
    container.hidden = true;
    if (fallback) fallback.hidden = false;
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
        projects.forEach((project) => {
          const placemark = new window.ymaps.Placemark(project.coordinates, {
            title: project.title,
            count: project.count,
            side: project.side,
            balloonContentHeader: project.title,
            balloonContentBody: project.count
          }, {
            iconLayout: markerLayout,
            iconOffset: project.offset,
            iconShape: {
              type: 'Rectangle',
              coordinates: [[-140, -60], [190, 80]]
            },
            hideIconOnBalloonOpen: false
          });
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
