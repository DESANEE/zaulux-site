import os, re

old_dir = "D:/AI/2nd-download-articles/articles2"
new_dir = "src/content/products"

numbered = {}
for f in os.listdir(new_dir):
    if not f.endswith('.mdx'): continue
    base = re.sub(r'^\d+-', '', f.replace('.mdx', ''))
    numbered[base] = f.replace('.mdx', '')

def clean_html(html):
    """Extract meaningful article content from Joomla article HTML"""
    # Remove script/style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<meta[^>]*>', '', html)
    
    # Remove navigation: Previous/Next
    html = re.sub(r'<ul class="pager[^"]*">.*?</ul>', '', html, flags=re.DOTALL)
    
    # Remove "Related Articles" section
    html = re.sub(r'<div class="relateditems[^"]*">.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
    
    # Remove H1 (title already shown)
    html = re.sub(r'<h1[^>]*>.*?</h1>', '', html)
    
    # Remove author/category meta
    html = re.sub(r'<span[^>]*>.*?admin.*?</span>', '', html, flags=re.DOTALL)
    html = re.sub(r'<a[^>]*>robot</a>|<a[^>]*>positioner</a>|<a[^>]*>.*?</a>', '', html)
    
    # Simplify: keep only meaningful tags
    # Keep p, ul, ol, li, strong, em, br, table, tr, td, th, h2, h3, h4
    tags_keep = ['p', 'ul', 'ol', 'li', 'strong', 'em', 'br', 'table', 'tr', 'td', 'th', 'h2', 'h3', 'h4', 'img']
    pattern = r'<(/?)(?!' + '|'.join(tags_keep) + r'\b)\w+[^>]*>'
    html = re.sub(pattern, '', html)
    
    # Clean up whitespace
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)
    html = re.sub(r'>\s+<', '>\n<', html)
    html = html.strip()
    
    # Remove empty divs
    html = re.sub(r'<div>\s*</div>', '', html)
    
    return html

updated = 0
for old_fname in sorted(os.listdir(old_dir)):
    if not old_fname.endswith('.html'): continue
    old_slug = old_fname.replace('.html', '')
    new_slug = numbered.get(old_slug)
    if not new_slug: continue
    
    with open(os.path.join(old_dir, old_fname), 'r', encoding='utf-8') as f:
        html = f.read()
    
    m = re.search(r'id="sp-component".*?(?=</section>)', html, re.DOTALL)
    if not m: continue
    
    cleaned = clean_html(m.group())
    
    # Read current MDX frontmatter
    mdx_path = os.path.join(new_dir, new_slug + '.mdx')
    with open(mdx_path, 'r', encoding='utf-8') as f:
        mdx = f.read()
    
    parts = mdx.split('---', 2)
    fm = parts[1] if len(parts) >= 2 else ''
    
    # Keep gallery
    gallery = ''
    gallery_match = re.search(r'## Product Gallery.*', mdx, re.DOTALL)
    if gallery_match:
        gallery = '\n\n' + gallery_match.group()
    
    new_mdx = f'---\n{fm.strip()}\n---\n\n{cleaned}\n{gallery}'
    
    with open(mdx_path, 'w', encoding='utf-8') as f:
        f.write(new_mdx)
    updated += 1

print(f"Cleaned {updated} MDX files")
