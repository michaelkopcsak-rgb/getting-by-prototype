"""Make app.html (iPhone, full-screen, Add to Home Screen) from index.html. Run after editing index.html."""
import pathlib, struct, zlib, math, re
d = pathlib.Path(__file__).parent
s = (d / 'index.html').read_text()
s = s.replace('<html lang="en">', '<html lang="en" class="app">', 1)
s = re.sub(r'<title>Getting By — Prototype v\d+</title>', '''<title>Getting By</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Getting By">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#F0F5F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1A16" media="(prefers-color-scheme: dark)">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="manifest" href="manifest.webmanifest">''', s, count=1)
assert 'class="app"' in s and 'apple-touch-icon' in s
(d / 'app.html').write_text(s)
(d / 'manifest.webmanifest').write_text('''{
  "name": "Getting By",
  "short_name": "Getting By",
  "start_url": "app.html",
  "scope": "./",
  "display": "standalone",
  "background_color": "#F0F5F2",
  "theme_color": "#1B4D3E",
  "icons": [{"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}]
}
''')
# App icon: deep jade square, soft "breath" rings (iOS rounds the corners itself)
def icon(n):
    bg, ring, core = (0x1B, 0x4D, 0x3E), (0xA9, 0xD3, 0xC2), (0xF0, 0xF5, 0xF2)
    rows = []
    for y in range(n):
        row = bytearray([0])
        for x in range(n):
            r = math.hypot(x - n / 2 + .5, y - n / 2 + .5) / n
            c = core if r < .17 else bg if r < .21 else ring if r < .25 else bg if r < .29 else tuple((a + b) // 2 for a, b in zip(ring, bg)) if r < .32 else bg
            row += bytes(c)
        rows.append(bytes(row))
    raw = zlib.compress(b''.join(rows), 9)
    ch = lambda t, b: struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + ch(b'IHDR', struct.pack('>IIBBBBB', n, n, 8, 2, 0, 0, 0)) + ch(b'IDAT', raw) + ch(b'IEND', b'')
for n in (180, 512):
    (d / f'icon-{n}.png').write_bytes(icon(n))
print('app.html, manifest, icons written')
