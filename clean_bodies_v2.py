import re, os

old_dir = "D:/AI/2nd-download-articles/articles2"

numbered = {}
for f in os.listdir("src/content/products"):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def clean_body(html):
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: return ""
    body = m.group()
    
    # 1. Script/style — always safe to remove
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    
    # 2. Admin/author name span
    body = re.sub(r'<span[^>]*>\s*<span[^>]*>\s*admin\s*</span>\s*</span>', '', body, flags=re.DOTALL)
    
    # 3. Hits/Ratings inline text (between time and article body)
    body = re.sub(r'Hits:\s*\d+', '', body)
    body = re.sub(r'Ratings\s*\(\d+\)', '', body)
    
    # 4. Old tag links (href contains /component/tags/ or /tag/)
    body = re.sub(r'<a\s[^>]*href="[^"]*(?:/component/tags/|/tag/)[^"]*"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    
    # 5. Prev/Next nav (pager ul)
    body = re.sub(r'<ul class="pager[^"]*">.*?</ul>', '', body, flags=re.DOTALL)
    
    # 6. "Previous article:" / "Next article:" text (without removing article body links)
    body = re.sub(r'<span[^>]*>\s*Previous article:\s*</span>', '', body)
    body = re.sub(r'<span[^>]*>\s*Next article:\s*</span>', '', body)
    body = re.sub(r'<span[^>]*>\s*Prev\s*</span>', '', body)
    body = re.sub(r'<span[^>]*>\s*Next\s*</span>', '', body)
    
    # 7. Social sharing div
    body = re.sub(r'<div class="article-social-share[^"]*">.*?</div>\s*</div>', '</div>', body, flags=re.DOTALL)
    
    # 8. "Related Articles" div
    body = re.sub(r'<div class="relateditems[^"]*">.*?</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # 9. Index.php links (but NOT article links that have content)
    body = re.sub(r'<a\s[^>]*href="/index\.php[^"]*"[^>]*>\s*</a>', '', body)
    # Remove index.php links only if they're tag/admin links (short text)
    body = re.sub(r'<a\s[^>]*href="[^"]*index\.php.*?option=com_tags[^"]*"[^>]*>[^<]*</a>', '', body, flags=re.DOTALL)
    
    # 10. Clean empty elements
    body = re.sub(r'<div[^>]*>\s*</div>', '', body)
    body = re.sub(r'<span[^>]*>\s*</span>', '', body)
    body = re.sub(r'<a[^>]*>\s*</a>', '', body)
    
    # 11. Remove H1 (title shown by template)
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body)
    
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
    body_map[new_slug] = clean_body(html)

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

# Verify text preserved
for slug in ['25-cradle-weld-positioner-cwp3', '19-welding-positioner-wp1']:
    if slug in body_map:
        import re as re2
        text = re2.sub(r'<[^>]+>', ' ', body_map[slug])
        text = re2.sub(r'\s+', ' ', text).strip()
        print(f'{slug}: {len(text)} chars -> {text[:120]}')
