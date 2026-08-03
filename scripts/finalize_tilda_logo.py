from pathlib import Path
import re
import shutil

root = Path('.')
source_svg_path = root / 'debug/logo-candidates/url-00.svg'
if not source_svg_path.exists():
    raise SystemExit('Original Tilda SVG candidate is missing')

original_svg = source_svg_path.read_text('utf-8').strip()
assets = root / 'assets'
assets.mkdir(exist_ok=True)
(assets / 'logo.svg').write_text(original_svg + '\n', 'utf-8')

inline_svg = re.sub(r'^<\?xml[^>]*>\s*', '', original_svg).strip()
inline_svg = inline_svg.replace('fill="#ffffff"', 'fill="currentColor"')
inline_svg = inline_svg.replace('stroke="#ffffff"', 'stroke="currentColor"')
inline_svg = re.sub(r'\swidth="[^"]+"', '', inline_svg, count=1)
inline_svg = re.sub(r'\sheight="[^"]+"', '', inline_svg, count=1)

def svg_with_class(class_name: str) -> str:
    return inline_svg.replace('<svg ', f'<svg class="{class_name}" aria-hidden="true" focusable="false" ', 1)

index_path = root / 'index.html'
index = index_path.read_text('utf-8')

header_logo = (
    '<a class="brand" href="#top" aria-label="313 — на главную">'
    + svg_with_class('brand-logo-svg')
    + '<span class="sr-only">313</span></a>'
)
index, header_count = re.subn(
    r'<a class="brand" href="#top" aria-label="313 — на главную">.*?</a>',
    header_logo,
    index,
    count=1,
    flags=re.S,
)
if header_count != 1:
    raise SystemExit('Header logo markup was not found exactly once')

footer_logo = (
    '<a class="footer-brand" href="#top" aria-label="313 — наверх">'
    + svg_with_class('footer-logo-svg')
    + '<span class="sr-only">313</span></a>'
)
index, footer_count = re.subn(
    r'<a class="footer-brand" href="#top">313</a>',
    footer_logo,
    index,
    count=1,
)
if footer_count != 1:
    raise SystemExit('Footer logo markup was not found exactly once')

project_head_old = (
    '<div class="section-head reveal"><div><p class="eyebrow">Наши работы</p>'
    '<h2 id="projects-title">Проекты</h2></div>'
    '<p class="section-intro">Все изображения собраны здесь. Проекты подгружаются постепенно, '
    'поэтому страница остаётся лёгкой и не превращается в бесконечный скроллер.</p></div>'
)
project_head_new = (
    '<div class="section-head section-head--single reveal"><div>'
    '<p class="eyebrow">Наши работы</p><h2 id="projects-title">Проекты</h2></div></div>'
)
if project_head_old not in index:
    raise SystemExit('Project intro text block was not found')
index = index.replace(project_head_old, project_head_new, 1)
index_path.write_text(index, 'utf-8')

styles_path = root / 'styles.css'
styles = styles_path.read_text('utf-8')
marker = '/* Original 313 logo from Tilda */'
if marker not in styles:
    styles += (
        '\n' + marker + '\n'
        '.brand-logo-svg{display:block;width:clamp(118px,9vw,154px);height:auto;flex:none}'
        '.footer-brand{display:block;line-height:0}'
        '.footer-logo-svg{display:block;width:clamp(220px,26vw,356px);height:auto}'
        '.section-head--single{grid-template-columns:1fr}'
        '@media(max-width:720px){.brand-logo-svg{width:112px}.footer-logo-svg{width:min(280px,70vw)}}\n'
    )
styles_path.write_text(styles, 'utf-8')

cleanup_files = [
    'TEMP_SOURCE_LINK.md',
    'logo-placeholder.svg',
    'SOURCE_URL.txt',
    'TEMP_LINK.html',
    'TEMP_README_LINK.md',
    'TEMP_LINK2.md',
    'scripts/fetch_tilda_source.py',
    'scripts/extract_logo_candidates.py',
    'scripts/finalize_tilda_logo.py',
    '.github/workflows/fetch-tilda-source.yml',
    '.github/workflows/extract-logo-candidates.yml',
    '.github/workflows/finalize-tilda-logo.yml',
]
for relative in cleanup_files:
    path = root / relative
    if path.exists():
        path.unlink()

if (root / 'debug').exists():
    shutil.rmtree(root / 'debug')

print('Installed original Tilda SVG logo, removed project intro, and cleaned temporary files')
