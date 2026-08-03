from pathlib import Path
import re

index_path = Path('index.html')
css_path = Path('hero-tilda.css')

index = index_path.read_text(encoding='utf-8')
css = css_path.read_text(encoding='utf-8')

map_section = '''
    <section class="section section-dark project-map" id="geography" aria-labelledby="geography-title">
      <div class="section-head reveal">
        <div>
          <p class="eyebrow">География проектов</p>
          <h2 id="geography-title">Карта проектов</h2>
        </div>
        <p class="section-intro">Нажмите на город, чтобы посмотреть проекты. Из списка можно сразу перейти к нужной работе.</p>
      </div>
      <div class="project-map__interactive reveal">
        <div class="project-map__frame">
          <div id="yandex-project-map" class="project-map__canvas" data-yandex-map data-api-key="" aria-label="Интерактивная Яндекс.Карта с географией проектов студии 313"></div>
          <div class="project-map__fallback" data-map-fallback hidden></div>
        </div>
        <aside class="project-map__projects" data-map-projects-panel hidden aria-live="polite" aria-label="Проекты выбранного города">
          <div class="project-map__projects-head">
            <div>
              <p class="eyebrow">Проекты города</p>
              <h3 data-map-city-title></h3>
              <p data-map-city-count></p>
            </div>
            <button type="button" class="project-map__projects-close" data-map-panel-close aria-label="Закрыть список проектов">×</button>
          </div>
          <div class="project-map__projects-list" data-map-project-list></div>
        </aside>
      </div>
      <div class="project-map__legend reveal" aria-label="Города и количество проектов">
        <button type="button" data-map-city="moscow"><span>Москва</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="ekaterinburg"><span>Екатеринбург</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="chelyabinsk"><span>Челябинск</span><strong>7 проектов</strong></button>
        <button type="button" data-map-city="miass"><span>Миасс</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="uvildy"><span>Увильды</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="chelyabinsk-region"><span>Челябинская область</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="massandra"><span>Массандра</span><strong>1 проект</strong></button>
        <button type="button" data-map-city="tel-aviv"><span>Тель-Авив</span><strong>1 проект</strong></button>
      </div>
    </section>
'''

index, count = re.subn(
    r'\n\s*<section class="section section-dark project-map" id="geography".*?</section>\s*',
    '\n' + map_section + '\n',
    index,
    count=1,
    flags=re.S,
)
if count != 1:
    raise RuntimeError('Project map section not found')

if 'src="project-navigation.js"' not in index:
    index = index.replace(
        '<script src="script.js" defer></script>',
        '<script src="script.js" defer></script>\n  <script src="project-navigation.js" defer></script>'
    )

marker = '/* 313 interactive map project navigation */'
styles = r'''

/* 313 interactive map project navigation */
.project-map__interactive{position:relative}
.project-map__projects{position:absolute;z-index:8;top:20px;right:20px;bottom:20px;width:min(370px,calc(100% - 40px));overflow:auto;padding:26px;background:rgba(14,45,51,.94);border:1px solid rgba(184,215,207,.4);box-shadow:0 22px 70px rgba(0,0,0,.24);backdrop-filter:blur(14px);animation:mapPanelIn .36s var(--ease) both}
.project-map__projects[hidden]{display:none}
.project-map__projects-head{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;padding-bottom:22px;border-bottom:1px solid rgba(241,238,231,.2)}
.project-map__projects-head h3{margin-top:8px;font-size:clamp(28px,3vw,46px);line-height:.95;letter-spacing:-.04em}
.project-map__projects-head [data-map-city-count]{margin-top:10px;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:#9fc8bd}
.project-map__projects-close{flex:0 0 auto;display:grid;place-items:center;width:42px;height:42px;border:1px solid rgba(241,238,231,.35);border-radius:50%;background:transparent;color:var(--paper);font-size:27px;line-height:1;cursor:pointer;transition:background .25s var(--ease),color .25s var(--ease),transform .25s var(--ease)}
.project-map__projects-close:hover{background:var(--paper);color:#15363d;transform:rotate(6deg)}
.project-map__projects-list{display:grid}
.project-map__project{display:grid;grid-template-columns:38px minmax(0,1fr) auto;align-items:center;gap:14px;width:100%;padding:18px 0;border:0;border-bottom:1px solid rgba(241,238,231,.17);background:transparent;color:var(--paper);text-align:left;cursor:pointer}
.project-map__project-index{font-size:10px;letter-spacing:.14em;color:#9fc8bd}
.project-map__project-title{font-size:17px;line-height:1.15}
.project-map__project-arrow{font-size:19px;transition:transform .25s var(--ease)}
.project-map__project:hover .project-map__project-arrow{transform:translate(4px,-4px)}
.project-map__legend button{display:flex;flex-direction:column;gap:6px;min-height:92px;padding:20px;border:0;border-right:1px solid rgba(241,238,231,.2);border-bottom:1px solid rgba(241,238,231,.2);background:transparent;color:var(--paper);text-align:left;cursor:pointer;transition:background .25s var(--ease),color .25s var(--ease)}
.project-map__legend button:hover,.project-map__legend button.is-active{background:#eef0e8;color:#15363d}
.project-map__legend button:hover span,.project-map__legend button.is-active span{color:rgba(21,54,61,.68)}
.project-map__legend button span{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:rgba(241,238,231,.68)}
.project-map__legend button strong{font-size:18px;font-weight:500}
.project-card.is-map-target{position:relative;z-index:2}
.project-card.is-map-target .project-media{box-shadow:0 0 0 4px #63b8a4,0 26px 80px rgba(21,54,61,.24)}
.project-card.is-map-target .project-meta h3{color:#24534f}
@keyframes mapPanelIn{from{opacity:0;transform:translateX(18px)}to{opacity:1;transform:translateX(0)}}
@media(max-width:980px){.project-map__projects{width:min(330px,calc(100% - 32px));top:16px;right:16px;bottom:16px;padding:22px}.project-map__legend button{min-height:92px;padding:20px}}
@media(max-width:700px){.project-map__interactive{display:flex;flex-direction:column}.project-map__projects{position:relative;inset:auto;width:auto;max-height:none;margin:16px -22px 0;padding:24px 22px;border-left:0;border-right:0;box-shadow:none;animation:mapPanelMobileIn .32s var(--ease) both}.project-map__projects-head h3{font-size:38px}.project-map__project{grid-template-columns:34px minmax(0,1fr) auto;padding:17px 0}.project-map__legend button{min-height:80px;padding:16px}.project-map__legend button strong{font-size:16px}}
@keyframes mapPanelMobileIn{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){.project-map__projects{animation:none}.project-map__projects-close,.project-map__project-arrow,.project-map__legend button{transition:none}.project-card.is-map-target .project-media{box-shadow:0 0 0 4px #63b8a4}}
'''
if marker not in css:
    css += styles

index_path.write_text(index, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')
