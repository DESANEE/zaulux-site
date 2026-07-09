import os, re, json

content_dir = 'src/content/products'
files = sorted(f for f in os.listdir(content_dir) if f.endswith('.mdx'))

cat_fixes = {}

products = []
for f in files:
    with open(os.path.join(content_dir, f), 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Parse frontmatter
    seps = [m.start() for m in re.finditer(r'\n---\n', content)]
    if len(seps) < 2:
        fm_end = content.index('---', 4) if '---' in content[4:] else len(content)
        fm_text = content[4:fm_end]
    else:
        fm_text = content[seps[0]+5:seps[1]]
    
    def get_field(name):
        m = re.search(name + r':\s*"(.+?)"', fm_text)
        return m.group(1) if m else ''
    
    title = get_field('title')
    category = cat_fixes.get(f.replace('.mdx',''), get_field('category'))
    description = get_field('description')
    
    if not category:
        m = re.search(r'category:\s*(\S+)', fm_text)
        category = m.group(1) if m else 'Uncategorised'
    
    # Extract images from frontmatter
    images = []
    in_images = False
    for line in fm_text.split('\n'):
        if line.strip().startswith('images:'):
            in_images = True
            continue
        if in_images:
            if line.strip().startswith('- url:'):
                url_match = re.search(r'url:\s*"?(.+?)"?\s*$', line)
                if url_match:
                    img_url = url_match.group(1)
                    if '/images/' in img_url:
                        img_url = img_url.split('/images/')[-1]
                    images.append(img_url)
            elif not line.strip().startswith('-') and line.strip() and ':' in line:
                in_images = False
    
    # Extract body
    body_parts = content.split('---', 2)
    body_raw = body_parts[2] if len(body_parts) >= 3 else ''
    gallery_idx = body_raw.find('## Product Gallery')
    if gallery_idx > 0:
        body_raw = body_raw[:gallery_idx].strip()
    
    # Clean up: remove import, headings, meta
    body_raw = re.sub(r'^import.*?\n', '', body_raw)
    body_raw = re.sub(r'^#\s+.*?\n', '', body_raw, flags=re.MULTILINE)
    body_raw = re.sub(r'^\*\*Category:.*?\*\*\s*\n', '', body_raw, flags=re.MULTILINE)
    body_raw = re.sub(r'^\*\*Article ID:.*?\*\*\s*\n', '', body_raw, flags=re.MULTILINE)
    body_raw = re.sub(r'^\*\*Published:.*?\*\*\s*\n', '', body_raw, flags=re.MULTILINE)
    body_raw = body_raw.strip()
    
    # Escape for JS string
    import html as html_mod
    body_escaped = body_raw.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
    products.append({
        'slug': f.replace('.mdx', ''),
        'title': title,
        'category': category,
        'description': description,
        'body': body_escaped,
        'images': [{"url": f"/images/{i}", "alt": i.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ')} for i in images] if images else [],
    })

# Write
lines = ['export const products = [']
for p in products:
    lines.append('  {')
    lines.append(f'    slug: "{p["slug"]}",')
    lines.append(f'    title: "{p["title"]}",')
    lines.append(f'    category: "{p["category"]}",')
    lines.append(f'    description: "{p["description"]}",')
    lines.append(f'    body: "{p["body"]}",')
    imgs_json = json.dumps(p["images"])
    lines.append(f'    images: {imgs_json},')
    lines.append('  },')
lines.append('];')

with open('src/data/product-list.ts', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'{len(products)} products written')
print(f'Sample body: {products[0]["body"][:200]}')
