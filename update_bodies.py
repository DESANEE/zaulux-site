import os, re, json

old_dir = "D:/AI/2nd-download-articles/articles2"

# Build old-slug → new-slug map
numbered = {}
for f in os.listdir("src/content/products"):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def extract_body(html):
    """Extract clean article body from Joomla HTML"""
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: return ""
    body = m.group()
    # Remove script/style
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<meta[^>]*>', '', body)
    # Remove nav
    body = re.sub(r'<ul class="pager[^"]*">.*?</ul>', '', body, flags=re.DOTALL)
    # Remove related items
    body = re.sub(r'<div class="relateditems[^"]*">.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
    # Remove H1
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body)
    # Remove empty divs
    body = re.sub(r'<div>\s*</div>', '', body)
    body = re.sub(r'id="sp-component"[^>]*>', '', body)
    body = body.strip()
    return body

# Read current product-list.ts structure
with open("src/data/product-list.ts", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Build new body map from old articles
body_map = {}
for old_fname in os.listdir(old_dir):
    if not old_fname.endswith('.html'): continue
    old_slug = old_fname.replace('.html', '')
    new_slug = numbered.get(old_slug)
    if not new_slug: continue
    with open(os.path.join(old_dir, old_fname), 'r', encoding='utf-8') as f:
        html = f.read()
    body_map[new_slug] = extract_body(html)

# Now update product-list.ts: replace body field for each product
new_lines = []
for line in lines:
    # Look for body field
    m = re.match(r'(\s+body:\s+)"(.*)",?$', line)
    if m and m.group(2):  # has content
        indent = m.group(1)
        # Find which product this line belongs to - scan backwards for slug
        slug = None
        for prev in reversed(new_lines):
            sm = re.search(r'slug:\s*"([^"]+)"', prev)
            if sm:
                slug = sm.group(1)
                break
        if slug and slug in body_map:
            new_body = body_map[slug]
            # Escape for JS string
            escaped = new_body.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            line = f'{indent}"{escaped}",\n'
    new_lines.append(line)

with open("src/data/product-list.ts", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print(f"Updated {len(body_map)} product bodies")
# Show sample
sample = body_map.get('19-welding-positioner-wp1', '')
print(f"Sample body ({len(sample)} chars): {sample[:150]}")
