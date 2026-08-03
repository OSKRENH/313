from pathlib import Path
from urllib.request import Request, urlopen

url = "https://go313.ru/"
request = Request(url, headers={"User-Agent": "Mozilla/5.0 (313 site migration)"})
with urlopen(request, timeout=30) as response:
    html = response.read()

output = Path("debug/tilda-source.html")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_bytes(html)
print(f"Saved {len(html)} bytes to {output}")
