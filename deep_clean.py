import re, os

old_dir = "D:/AI/2nd-download-articles/articles2"

numbered = {}
for f in os.listdir("src/content/products"):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def deep_clean(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<meta[^>]*>', '', html)
    html = re.sub(r'<span[^>]*>.*?admin.*?</span>', '', html, flags=re.DOTALL)
    html = re.sub(r'Hits:\s*\d+', '', html)
    html = re.sub(r'Ratings\s*\(?\d*\)?', '', html)
    html = re.sub(r'<ul class="pager[^"]*">.*?</ul>', '', html, flags=re.DOTALL)
    html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="article-social-share[^"]*">.*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="relateditems[^"]*">.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<a[^>]*href="[^"]*(?:tag|component/tags|desanee\.com|index\.php)[^"]*"[^>]*>.*?</a>', '', html)
    html = re.sub(r'Previous article:.*?<a[^>]*>.*?</a>', '', html)
    html = re.sub(r'Next article:.*?<a[^>]*>.*?</a>', '', html)
    html = re.sub(r'Prev\s*\n?\s*Next', '', html)
    html = re.sub(r'<div>\s*</div>', '', html)
    html = re.sub(r'<div[^>]*>\s*</div>', '', html)
    html = re.sub(r'<h1[^>]*>.*?</h1>', '', html)
    html = re.sub(r'id="sp-component"[^>]*>', '', html)
    html = re.sub(r'\n\s*\n\s*\n+', '\n\n', html)
    return html.strip()

# Build body map
body_map = {}
for old_fname in os.listdir(old_dir):
    if not old_fname.endswith('.html'): continue
    old_slug = old_fname.replace('.html', '')
    new_slug = numbered.get(old_slug)
    if not new_slug: continue
    with open(os.path.join(old_dir, old_fname), 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: continue
    body_map[new_slug] = deep_clean(m.group())

# Update product-list.ts
with open("src/data/product-list.ts", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
current_slug = None
for line in lines:
    sm = re.search(r'slug:\s*"([^"]+)"', line)
    if sm:
        current_slug = sm.group(1)
    
    m = re.match(r'(\s+body:\s+)"(.*)",?$', line)
    if m and current_slug and current_slug in body_map:
        indent = m.group(1)
        new_body = body_map[current_slug]
        bs = chr(92)
        escaped = new_body.replace(bs, bs + bs).replace('"', bs + '"').replace('\n', bs + 'n')
        line = f'{indent}"{escaped}",' + '\n'
    new_lines.append(line)

with open("src/data/product-list.ts", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Deep cleaned {len(body_map)} bodies")
sample = body_map.get('24-pipe-positioner-pp3', '')
print(f"Sample ({len(sample)}): {sample[:250]}")
