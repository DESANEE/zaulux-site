import os, json, random

def find_image(filename):
    for root, dirs, files in os.walk('public/images'):
        for f in files:
            if f.lower() == filename.lower() and '_thumbnail' not in f.lower():
                rel = os.path.relpath(os.path.join(root, f), 'public/images')
                return '/images/' + rel.replace(chr(92), '/')
    return None

layout = {
    "Positioners": [
        ["wp-00.jpg","wp-04.jpg","wp-14.jpg","wp-24.jpg"],
        ["wp-18.jpg","wp-28.jpg","wp-36.jpg","wp-16.jpg"],
        ["wp-26.jpg","wp-43.jpg","wp-45.jpg","wp-12.jpg"],
    ],
    "Turning Rolls": [
        ["wr00-11.jpg","12wr00-10.jpg","wr00-20.jpg","wr00-37.jpg"],
        ["wr00-25.jpg","12wr00-18.jpg","12wr00-29.jpg","12wr00-36.jpg"],
        ["wr00-32.jpg","wr00-33.jpg","wr00-41.jpg","wr00-28.jpg"],
    ],
    "Manipulators": [
        ["wm-01.jpg","wm-02.jpg","wm-03.jpg","wp-04.jpg"],
        ["wm-05.jpg","wm-06.jpg","wm-07.jpg","wp-08.jpg"],
    ],
    "H-Beam Lines": [
        ["hbeam-11.jpg","hbeam-12.jpg","hbeam-13.jpg","hbeam-14.jpg"],
        ["hbeam-15.jpg","hbeam-02.jpg","hbeam-03.jpg","hbeam-04.jpg"],
        ["CNC-00.jpg","CNC-01.jpg","CNC-04.jpg","CNC-05.jpg"],
    ],
    "Robot Welding": [
        ["RCM-00.jpg","RCM-01.jpg","RCM-02.jpg","RCM-03.jpg"],
        ["RCM-04.jpg","RCM-05.jpg","RCM-06.jpg","RCM-07.jpg"],
    ],
    "Automation": [
        ["LASER tractor.jpg","LASER tractor-1.jpg","monitor-01.jpg","monitor-03.jpg"],
        ["monitor-00.jpg","LASER tractor-2.jpg","monitor-02.jpg","monitor-04.jpg"],
    ],
    "Beveling M/C": [
        ["xbj-00.jpg","xbj-01.jpg","xbj-02.jpg","xbj-03.jpg"],
        ["dx-03.jpg","dx-04.jpg","dx-05.jpg","dx-00.jpg"],
    ],
    "Combo Manipulator": [
        ["cbm-03.jpg","cbm-04.jpg","cbm-05.jpg","cbm-06.jpg"],
        ["cbm-13.jpg","cbm-14.jpg","cbm-17.jpg","cbm-18.jpg"],
        ["cbm-24.jpg","cbm-27.jpg","cbm-30.jpg","cbm-48.jpg"],
        ["cbm-52.jpg","cbm-53.jpg","cbm-55.jpg","cbm-50.jpg"],
    ],
}

result = []
all_images = []
missing = []
os.chdir('D:/AI/zaulux-site')

for cat_name, rows in layout.items():
    cat_result = {"category": cat_name, "rows": []}
    for row in rows:
        img_row = []
        for fname in row:
            path = find_image(fname)
            if path:
                img_row.append(path)
                all_images.append(path)
            else:
                missing.append(f'{cat_name}: {fname}')
        if img_row:
            cat_result["rows"].append(img_row)
    result.append(cat_result)

for c in result:
    total = sum(len(r) for r in c["rows"])
    print(f'{c["category"]}: {len(c["rows"])} rows, {total} images')
print(f'\nTotal: {len(all_images)} images, Missing: {len(missing)}')
for m in missing:
    print(f'  MISSING: {m}')

random.seed(42)
random.shuffle(all_images)

with open('public/gallery-data.json', 'w') as f:
    json.dump({"categories": result, "all": all_images}, f)
print('\nDone')
