from pathlib import Path

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
        <p class="section-intro">Проектируем пространства в России и за её пределами. На карте отмечены города и регионы уже реализованных проектов.</p>
      </div>
      <div class="project-map__viewport reveal" tabindex="0" aria-label="Карта проектов. На мобильном устройстве карту можно двигать по горизонтали.">
        <img src="assets/projects-map.svg" alt="Карта проектов студии 313: Москва, Екатеринбург, Челябинск, Миасс, Увильды, Массандра и Тель-Авив" loading="lazy" decoding="async" />
      </div>
      <div class="project-map__legend reveal" aria-label="Список городов и количества проектов">
        <div><span>Москва</span><strong>1 проект</strong></div>
        <div><span>Екатеринбург</span><strong>1 проект</strong></div>
        <div><span>Челябинск</span><strong>7 проектов</strong></div>
        <div><span>Миасс</span><strong>1 проект</strong></div>
        <div><span>Увильды</span><strong>1 проект</strong></div>
        <div><span>Челябинская область</span><strong>1 проект</strong></div>
        <div><span>Массандра</span><strong>1 проект</strong></div>
        <div><span>Тель-Авив</span><strong>1 проект</strong></div>
      </div>
    </section>
'''

if 'id="geography"' not in index:
    index = index.replace('  </main>', map_section + '  </main>')

marker = '/* 313 header logo reveal and project map */'
map_css = r'''

/* 313 header logo reveal and project map */
.brand{transition:opacity .38s var(--ease),transform .38s var(--ease),visibility .38s var(--ease)}
.site-header:not(.is-scrolled):not(.menu-open) .brand{opacity:0;visibility:hidden;pointer-events:none;transform:translateY(-8px)}
.site-header.is-scrolled .brand,.site-header.menu-open .brand{opacity:1;visibility:visible;pointer-events:auto;transform:translateY(0)}
.project-map{position:relative;overflow:hidden;background:#15363d;color:var(--paper);border-top:1px solid rgba(241,238,231,.18)}
.project-map::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 72% 18%,rgba(100,184,164,.12),transparent 38%);pointer-events:none}
.project-map>.section-head,.project-map__viewport,.project-map__legend{position:relative;z-index:1}
.project-map__viewport{overflow:hidden;border:1px solid rgba(184,215,207,.24);background:#15363d}
.project-map__viewport img{display:block;width:100%;height:auto;min-height:0;object-fit:contain}
.project-map__legend{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:30px;border-top:1px solid rgba(241,238,231,.2);border-left:1px solid rgba(241,238,231,.2)}
.project-map__legend div{display:flex;flex-direction:column;gap:6px;min-height:92px;padding:20px;border-right:1px solid rgba(241,238,231,.2);border-bottom:1px solid rgba(241,238,231,.2)}
.project-map__legend span{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:rgba(241,238,231,.68)}
.project-map__legend strong{font-size:18px;font-weight:500}
@media(max-width:980px){.project-map__viewport{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none}.project-map__viewport::-webkit-scrollbar{display:none}.project-map__viewport img{width:auto;min-width:920px;max-width:none}.project-map__legend{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.site-header:not(.is-scrolled):not(.menu-open) .brand{transform:translateY(-5px)}.project-map__viewport{margin-left:-22px;margin-right:-22px;border-left:0;border-right:0}.project-map__viewport img{min-width:820px}.project-map__legend{grid-template-columns:1fr 1fr;margin-top:22px}.project-map__legend div{min-height:80px;padding:16px}.project-map__legend strong{font-size:16px}}
@media(prefers-reduced-motion:reduce){.brand{transition:none!important}}
'''

if marker not in css:
    css += map_css

index_path.write_text(index, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')
