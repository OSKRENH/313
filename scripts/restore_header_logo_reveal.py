from pathlib import Path

path = Path('hero-tilda.css')
css = path.read_text(encoding='utf-8')
marker = '/* 313 header logo reveal */'
rules = '''

/* 313 header logo reveal */
.brand{transition:opacity .38s var(--ease),transform .38s var(--ease),visibility .38s var(--ease)}
.site-header:not(.is-scrolled):not(.menu-open) .brand{opacity:0;visibility:hidden;pointer-events:none;transform:translateY(-8px)}
.site-header.is-scrolled .brand,.site-header.menu-open .brand{opacity:1;visibility:visible;pointer-events:auto;transform:translateY(0)}
@media(max-width:700px){.site-header:not(.is-scrolled):not(.menu-open) .brand{transform:translateY(-5px)}}
@media(prefers-reduced-motion:reduce){.brand{transition:none!important}}
'''
if marker not in css:
    css += rules
path.write_text(css, encoding='utf-8')
