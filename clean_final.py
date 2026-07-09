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
    
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    
    # 1. Author name
    body = re.sub(r'<span[^>]*>\s*<span itemprop="name"[^>]*>\s*admin\s*</span>\s*</span>', '', body, flags=re.DOTALL)
    
    # 2. Hits counter
    body = re.sub(r'<span[^>]*>\s*Hits:\s*\d+\s*</span>', '', body)
    
    # 3. Ratings + social share
    body = re.sub(r'<div class="article-ratings-social-share[^"]*">.*?</div>\s*</div>\s*</div>', '</div>', body, flags=re.DOTALL)
    
    # 4. "Previous article:" / "Next article:" nav
    body = re.sub(r'<span class="visually-hidden"[^>]*>\s*Previous article:.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="visually-hidden"[^>]*>\s*Next article:.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<a class="btn btn-sm btn-secondary prev"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    body = re.sub(r'<a class="btn btn-sm btn-secondary next"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span aria-hidden="true">\s*Prev\s*</span>', '', body)
    body = re.sub(r'<span aria-hidden="true">\s*Next\s*</span>', '', body)
    
    # 5. Related articles
    body = re.sub(r'<div class="related-article-list-container">.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # 6. Tag links
    body = re.sub(r'<a\s[^>]*href="[^"]*option=com_tags[^"]*"[^>]*>[^<]*</a>', '', body, flags=re.DOTALL)
    body = re.sub(r'<a\s[^>]*href="[^"]*component/tags/[^"]*"[^>]*>[^<]*</a>', '', body, flags=re.DOTALL)
    
    # 7. Category link (index.php)
    body = re.sub(r'<a\s[^>]*href="[^"]*option=com_content[^"]*"[^>]*>\s*[^<]{1,20}\s*</a>', '', body, flags=re.DOTALL)
    
    # 8. H1
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body)
    
    # 9. Bootstrap carousel (images shown in Product Gallery)
    body = re.sub(r'<div class="article-feature-gallery"[^>]*>.*?</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # 10. Carousel control "Previous" / "Next" (visually-hidden spans)
    body = re.sub(r'<span class="visually-hidden">\s*Previous\s*</span>', '', body)
    body = re.sub(r'<span class="visually-hidden">\s*Next\s*</span>', '', body)
    
    # 11. Clean up
    body = re.sub(r'<div[^>]*>\s*</div>', '', body)
    body = re.sub(r'\n\s*\n\s*\n+', '\n\n', body)
    body = body.strip()
    body = body.replace('/DSiamge/', '/')
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
    if sm: current_slug = sm.group(1)
    m = re.match(r'(\s+body:\s+)"(.*)",?$', line)
    if m and current_slug and current_slug in body_map:
        indent = m.group(1)
        new_body = body_map[current_slug]
        bs = chr(92)
        escaped = new_body.replace(bs, bs + bs).replace('"', bs + '"').replace('\n', bs + 'n')
        line = indent + '"' + escaped + '",\n'
    new_lines.append(line)

with open("src/data/product-list.ts", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Verify
for slug in ['25-cradle-weld-positioner-cwp3', '19-welding-positioner-wp1']:
    if slug in body_map:
        text = re.sub(r'<[^>]+>', ' ', body_map[slug])
        text = re.sub(r'\s+', ' ', text).strip()
        bad = ['admin', 'Hits:', 'Previous article', 'Next article', 'Prev', 'Next']
        found = [b for b in bad if b in text]
        status = 'CLEAN' if not found else f'HAS: {found}'
        print(f'{slug}: {len(text)} chars, {status}')
