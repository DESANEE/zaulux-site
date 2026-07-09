import sys, re, urllib.request

html = urllib.request.urlopen("https://www.zaulux.com/products/25-cradle-weld-positioner-cwp3/").read().decode()

m = re.search(r'class="article-content"[^>]*>(.*?)</div>\s*<', html, re.DOTALL)
if m:
    text = re.sub(r'<[^>]+>', ' ', m.group(1))
    # Unescape JSON escapes
    text = text.replace('\\n', ' ').replace('\\t', ' ').replace('\\"', '"').replace('\\\\', '')
    text = re.sub(r'\s+', ' ', text).strip()
    print(f'Content: {len(text)} chars')
    print(text[:600])
else:
    print('Not found')
    # Try broader search
    m2 = re.search(r'Product Details.*?image-gallery', html, re.DOTALL)
    if m2:
        t = re.sub(r'<[^>]+>', ' ', m2.group())
        t = re.sub(r'\s+', ' ', t).strip()
        print(f'Product Details area ({len(t)}): {t[:400]}')
