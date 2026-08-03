from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
import html as html_module
import re

source_path = Path("debug/tilda-source.html")
source = source_path.read_text("utf-8", errors="replace")
base_url = "https://go313.ru/"
out_dir = Path("debug/logo-candidates")
out_dir.mkdir(parents=True, exist_ok=True)

url_patterns = [
    r'''(?:https?:)?//[^\s"'<>]+?\.svg(?:\?[^\s"'<>]*)?''',
    r'''(?:(?:src|data-original|data-src|href)=["'])([^"']+?\.svg(?:\?[^"']*)?)["']''',
    r'''url\(["']?([^\)"']+?\.svg(?:\?[^\)"']*)?)["']?\)''',
]

found = []
for pattern in url_patterns:
    for match in re.finditer(pattern, source, flags=re.I):
        value = match.group(1) if match.lastindex else match.group(0)
        value = html_module.unescape(value)
        if value.startswith("//"):
            value = "https:" + value
        else:
            value = urljoin(base_url, value)
        pos = match.start()
        if value not in [item[0] for item in found]:
            found.append((value, pos))

inline = []
for match in re.finditer(r'<svg\b[^>]*>.*?</svg>', source, flags=re.I | re.S):
    svg = match.group(0)
    context = re.sub(r'\s+', ' ', source[max(0, match.start()-300):match.start()+100])
    inline.append((svg, match.start(), context))

report = [f"SVG URL candidates: {len(found)}", f"Inline SVG candidates: {len(inline)}", ""]
headers = {"User-Agent": "Mozilla/5.0 (313 site migration)"}
for index, (url, pos) in enumerate(sorted(found, key=lambda item: item[1])):
    context = re.sub(r'<[^>]+>', ' ', source[max(0, pos-240):pos+360])
    context = re.sub(r'\s+', ' ', html_module.unescape(context)).strip()
    report.append(f"## URL {index:02d}\nPosition: {pos}\nURL: {url}\nContext: {context[:500]}\n")
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=25) as response:
            data = response.read()
        if b"<svg" in data[:1000].lower() or url.lower().split('?')[0].endswith('.svg'):
            (out_dir / f"url-{index:02d}.svg").write_bytes(data)
    except Exception as error:
        report.append(f"Download error: {error}\n")

for index, (svg, pos, context) in enumerate(inline):
    (out_dir / f"inline-{index:02d}.svg").write_text(svg, "utf-8")
    report.append(f"## INLINE {index:02d}\nPosition: {pos}\nContext: {context[:500]}\n")

Path("debug/logo-candidates.md").write_text("\n".join(report), "utf-8")
print(f"Found {len(found)} URL SVGs and {len(inline)} inline SVGs")
