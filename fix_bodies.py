import re, os

old_dir = "D:/AI/2nd-download-articles/articles2"

numbered = {}
for f in os.listdir("src/content/products"):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def extract_body(html):
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: return ""
    body = m.group()
    # ONLY remove these specific problematic elements:
    # 1. Script/style
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    # 2. Tag links (href contains /component/tags/ or /tag/)
    body = re.sub(r'<a[^>]*href="[^"]*(?:/component/tags/|/tag/)[^"]*"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    # 3. Prev/Next navigation
    body = re.sub(r'<ul class="pager[^"]*">.*?</ul>', '', body, flags=re.DOTALL)
    # 4. Article info links (point to /index.php)
    body = re.sub(r'<a[^>]*href="[^"]*index\.php[^"]*"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    # 5. Remove empty <a> tags left after cleanup
    body = re.sub(r'<a[^>]*>\s*</a>', '', body)
    body = body.strip()
    return body

# Build body map
body_map = {}
for old_fname in os.listdir(old_dir):
    if not old_fname.endswith('.html'): continue
    old_slug = old_fname.replace('.html', '')
    new_slug = numbered.get(old_slug)
    if not new_slug: continue
    with open(os.path.join(old_dir, old_fname), 'r', encoding='utf-8') as f:
        html = f.read()
    body_map[new_slug] = extract_body(html)

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
        line = f'{indent}"{escaped}",\n'
    new_lines.append(line)

with open("src/data/product-list.ts", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Targeted cleanup on {len(body_map)} bodies")
sample = body_map.get('25-cradle-weld-positioner-cwp3', '')
import re as re2
text = re2.sub(r'<[^>]+>', ' ', sample)
text = re2.sub(r'\s+', ' ', text).strip()
print(f"Sample text ({len(text)}): {text[:200]}")
