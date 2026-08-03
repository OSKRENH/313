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
        <p class="section-intro">Проектируем пространства в России и за её пределами. На карте отмечены города и регионы реализованных проектов.</p>
      </div>
      <div class="project-map__frame reveal">
        <div id="yandex-project-map" class="project-map__canvas" data-yandex-map data-api-key="" aria-label="Интерактивная Яндекс.Карта с географией проектов студии 313"></div>
        <div class="project-map__fallback" data-map-fallback hidden>
          <p>Карта временно недоступна.</p>
          <a href="https://yandex.ru/maps/?ll=47.500000%2C51.500000&z=3" target="_blank" rel="noreferrer">Открыть географию в Яндекс.Картах ↗</a>
        </div>
      </div>
      <div class="project-map__legend reveal" aria-label="Города и количество проектов">
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

# Remove the previous static map section wherever it is located.
index = re.sub(
    r'\n\s*<section class="section section-dark project-map" id="geography".*?</section>\s*',
    '\n',
    index,
    count=1,
    flags=re.S,
)

# Place the new Yandex map directly after the authors section.
authors_pattern = r'(<section class="authors section section-dark" id="authors".*?</section>)'
if not re.search(authors_pattern, index, flags=re.S):
    raise RuntimeError('Authors section not found')
index = re.sub(authors_pattern, r'\1\n' + map_section, index, count=1, flags=re.S)

footer = '''
  <footer class="site-footer">
    <a class="footer-brand" href="#top" aria-label="313 — в начало сайта">
      <img src="assets/logo.svg" alt="313" />
    </a>
    <p>© <span data-year></span> All Rights Reserved.</p>
    <a class="back-to-top" href="#top" aria-label="Перейти в начало сайта">
      <span class="back-to-top__icon" aria-hidden="true">↑</span>
      <span>В начало</span>
    </a>
  </footer>
'''
index, footer_count = re.subn(r'\s*<footer class="site-footer">.*?</footer>', '\n' + footer, index, count=1, flags=re.S)
if footer_count != 1:
    raise RuntimeError('Footer not found')

if 'src="yandex-map.js"' not in index:
    index = index.replace('<script src="script.js" defer></script>', '<script src="yandex-map.js" defer></script>\n  <script src="script.js" defer></script>')

marker = '/* 313 Yandex map and SVG footer */'
new_css = r'''

/* 313 Yandex map and SVG footer */
.project-map{position:relative;overflow:hidden;background:#15363d;color:var(--paper);border-top:1px solid rgba(241,238,231,.18)}
.project-map::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 72% 18%,rgba(100,184,164,.14),transparent 40%);pointer-events:none}
.project-map>.section-head,.project-map__frame,.project-map__legend{position:relative;z-index:1}
.project-map__frame{position:relative;height:clamp(520px,62vw,760px);overflow:hidden;border:1px solid rgba(184,215,207,.28);background:#0e2d33}
.project-map__canvas{width:100%;height:100%;opacity:0;transition:opacity .7s var(--ease)}
.project-map__canvas.is-ready{opacity:1}
.project-map__canvas [class*="ground-pane"]{filter:grayscale(1) sepia(.48) hue-rotate(104deg) saturate(.82) brightness(.62) contrast(1.14)}
.project-map__canvas [class*="copyright"],.project-map__canvas [class*="controls__control"]{filter:none}
.project-map__canvas [class*="map-copyrights-promo"]{display:none!important}
.project-map__fallback{position:absolute;inset:0;display:grid;place-content:center;gap:14px;text-align:center;background:linear-gradient(145deg,#15363d,#0e2d33)}
.project-map__fallback[hidden]{display:none}
.project-map__fallback p{font-size:22px}
.project-map__fallback a{font-size:13px;text-transform:uppercase;letter-spacing:.12em;text-decoration:underline;text-underline-offset:5px}
.ya-project-marker{position:relative;width:20px;height:20px;color:#eef0e8;font-family:Arial,Helvetica,sans-serif;pointer-events:auto}
.ya-project-marker__dot{position:absolute;inset:3px;border:3px solid #15363d;border-radius:50%;background:#eef0e8;box-shadow:0 0 0 1px rgba(238,240,232,.25)}
.ya-project-marker__pulse{position:absolute;inset:-8px;border:1px solid rgba(130,184,171,.8);border-radius:50%;animation:yaMapPulse 2.7s ease-out infinite}
.ya-project-marker__label{position:absolute;top:50%;display:flex;flex-direction:column;gap:3px;min-width:max-content;padding:8px 10px;background:rgba(21,54,61,.88);border:1px solid rgba(184,215,207,.32);backdrop-filter:blur(7px);transform:translateY(-50%)}
.ya-project-marker__label strong{font-size:12px;line-height:1;text-transform:uppercase;letter-spacing:.08em;font-weight:600}
.ya-project-marker__label small{font-size:9px;line-height:1;text-transform:uppercase;letter-spacing:.1em;color:#9fc8bd}
.ya-project-marker--right .ya-project-marker__label,.ya-project-marker--right-up .ya-project-marker__label,.ya-project-marker--right-down .ya-project-marker__label,.ya-project-marker--right-down-far .ya-project-marker__label{left:28px}
.ya-project-marker--left-up .ya-project-marker__label,.ya-project-marker--left-down .ya-project-marker__label{right:28px;text-align:right}
.ya-project-marker--right-up .ya-project-marker__label,.ya-project-marker--left-up .ya-project-marker__label{top:-20px}
.ya-project-marker--right-down .ya-project-marker__label,.ya-project-marker--left-down .ya-project-marker__label{top:42px}
.ya-project-marker--right-down-far .ya-project-marker__label{top:72px}
@keyframes yaMapPulse{0%{opacity:.8;transform:scale(.55)}75%,100%{opacity:0;transform:scale(1.45)}}
.project-map__legend{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:30px;border-top:1px solid rgba(241,238,231,.2);border-left:1px solid rgba(241,238,231,.2)}
.project-map__legend div{display:flex;flex-direction:column;gap:6px;min-height:92px;padding:20px;border-right:1px solid rgba(241,238,231,.2);border-bottom:1px solid rgba(241,238,231,.2)}
.project-map__legend span{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:rgba(241,238,231,.68)}
.project-map__legend strong{font-size:18px;font-weight:500}
.site-footer{background:#15363d;color:var(--paper);border-top:1px solid rgba(241,238,231,.2);padding:clamp(38px,5vw,72px) var(--pad);align-items:end}
.footer-brand{display:block;width:clamp(190px,29vw,520px);font-size:0;line-height:0;letter-spacing:0}
.footer-brand img{display:block;width:100%;height:auto}
.site-footer p{color:rgba(241,238,231,.68)}
.back-to-top{justify-self:end;display:flex!important;align-items:center;gap:13px;font-size:12px;text-transform:uppercase;letter-spacing:.12em}
.back-to-top__icon{display:grid;place-items:center;width:54px;height:54px;border:1px solid rgba(241,238,231,.55);border-radius:50%;font-size:22px;transition:background .3s var(--ease),color .3s var(--ease),transform .3s var(--ease)}
.back-to-top:hover .back-to-top__icon{background:var(--paper);color:#15363d;transform:translateY(-4px)}
@media(max-width:980px){.project-map__frame{height:620px}.project-map__legend{grid-template-columns:repeat(2,minmax(0,1fr))}.ya-project-marker__label{display:none}.site-footer{grid-template-columns:1fr auto;gap:30px}.site-footer p{grid-column:1}.back-to-top{grid-column:2;grid-row:1 / span 2}}
@media(max-width:700px){.project-map__frame{height:520px;margin-left:-22px;margin-right:-22px;border-left:0;border-right:0}.project-map__legend{grid-template-columns:1fr 1fr;margin-top:22px}.project-map__legend div{min-height:80px;padding:16px}.project-map__legend strong{font-size:16px}.site-footer{grid-template-columns:1fr;padding:46px 22px;align-items:start}.footer-brand{width:min(76vw,360px)}.site-footer p,.back-to-top{grid-column:1;grid-row:auto}.back-to-top{justify-self:start;margin-top:22px}.back-to-top__icon{width:58px;height:58px}}
@media(prefers-reduced-motion:reduce){.project-map__canvas{transition:none}.ya-project-marker__pulse{animation:none}.back-to-top__icon{transition:none}}
'''

# Remove the previous custom-map override block and append the new version.
css = re.sub(r'/\* 313 header logo reveal and project map \*/.*?(?=/\*|\Z)', '', css, flags=re.S)
if marker not in css:
    css += new_css

index_path.write_text(index, encoding='utf-8')
css_path.write_text(css, encoding='utf-8')
