import re, os

old_dir = "D:/AI/2nd-download-articles/articles2"
numbered = {}
for f in os.listdir("src/content/products"):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def extract_clean_body(html):
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: return ""
    body = m.group()
    
    # Remove ALL Joomla wrapper divs, carousel, nav, social, tags, etc.
    # Keep only: <p>, <h2-4>, <ul>, <li>, <img>, <strong>, <em>
    
    # Remove scripts/styles
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body, flags=re.DOTALL)
    
    # Remove carousel
    body = re.sub(r'<div class="article-feature-gallery".*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # Remove ratings/social share
    body = re.sub(r'<div class="article-ratings-social-share.*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # Remove nav
    body = re.sub(r'<nav class="pagenavigation".*?</nav>', '', body, flags=re.DOTALL)
    
    # Remove related articles
    body = re.sub(r'<h3 class="related-article-title".*?</h3>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="article-list related-article-list".*?</div>\s*</div>\s*</div>', '', body, flags=re.DOTALL)
    
    # Remove tag list
    body = re.sub(r'<ul class="tags[^"]*">.*?</ul>', '', body, flags=re.DOTALL)
    
    # Remove H1
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body)
    
    # Remove admin, category, date spans
    body = re.sub(r'<span[^>]*itemprop="name"[^>]*>.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="category-name"[^>]*>.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="published"[^>]*>.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span[^>]*>\s*Hits:.*?</span>', '', body, flags=re.DOTALL)
    
    # Remove "Previous article / Next article" spans and buttons
    body = re.sub(r'<span class="visually-hidden">\s*Previous article:.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<span class="visually-hidden">\s*Next article:.*?</span>', '', body, flags=re.DOTALL)
    body = re.sub(r'<a class="btn[^"]*prev[^"]*"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    body = re.sub(r'<a class="btn[^"]*next[^"]*"[^>]*>.*?</a>', '', body, flags=re.DOTALL)
    
    # Remove carousel controls
    body = re.sub(r'<button class="carousel-control[^"]*"[^>]*>.*?</button>', '', body, flags=re.DOTALL)
    
    # Remove empty tags
    body = re.sub(r'<(div|span|a)\b[^>]*>\s*</\1>', '', body)
    
    # Remove wrapper divs without content
    body = re.sub(r'<div class="sp-column"[^>]*>\s*</div>', '', body)
    body = re.sub(r'<div class="article-details[^"]*"[^>]*>\s*</div>', '', body)
    
    # Remove id wrapper text
    body = re.sub(r'id="sp-component"[^>]*>\s*', '', body)
    
    # Extract all images — keep them
    images_html = ''
    for img in re.finditer(r'<img[^>]+>', body):
        src = re.search(r'src="([^"]+)"', img.group())
        if src:
            url = src.group(1).replace('/DSiamge/', '/')
            alt = re.search(r'alt="([^"]*)"', img.group())
            alt_text = alt.group(1) if alt else ''
            images_html += f'<img src="{url}" alt="{alt_text}" />\n'
    
    # Extract text paragraphs
    paragraphs = []
    current_text = ''
    for line in body.split('\n'):
        line = line.strip()
        if not line: continue
        # Skip lines that are just structural/wrapper tags
        if re.match(r'^<(meta|link|div|span|nav|button|a\b)[ >]', line): continue
        if re.match(r'^</?(div|span|nav|a)\b', line): continue
        # Extract text content — keep li, td, th, h2-h4, p, strong, em
        text = re.sub(r'<[^>]+>', ' ', line)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 5:
            paragraphs.append(text)
    
    # Build clean body: text paragraphs + images
    result = ''
    for p in paragraphs:
        # Skip Hits/admin lines
        if re.match(r'^(Hits:|admin\b|Published:)', p): continue
        if p not in result:
            result += f'<p>{p}</p>\n'
    
    if images_html:
        result += f'\n<div class="article-images">\n{images_html}</div>'
    
    result = result.strip()
    if not result:
        # Fallback: just use whatever's left after cleaning
        result = re.sub(r'\n\s*\n+', '\n\n', body).strip()
    
    return result

body_map = {}
for old_fname in os.listdir(old_dir):
    if not old_fname.endswith('.html'): continue
    old_slug = old_fname.replace('.html', '')
    new_slug = numbered.get(old_slug)
    if not new_slug: continue
    with open(os.path.join(old_dir, old_fname), 'r', encoding='utf-8') as f:
        html = f.read()
    body_map[new_slug] = extract_clean_body(html)

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
        escaped = new_body.replace('"', '\\"').replace('\n', '\\n')
        line = indent + '"' + escaped + '",\n'
    new_lines.append(line)

with open("src/data/product-list.ts", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

for slug in ['25-cradle-weld-positioner-cwp3', '19-welding-positioner-wp1']:
    if slug in body_map:
        text = re.sub(r'<[^>]+>', ' ', body_map[slug])
        text = re.sub(r'\s+', ' ', text).strip()
        print(f'{slug}: {len(text)} chars -> {text[:150]}')
