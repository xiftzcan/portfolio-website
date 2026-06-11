import re

with open('assets/js/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Split en and tr blocks
en_match = re.search(r'"en"\s*:\s*\{(.*)\n\s*"tr"\s*:\s*\{', content, re.DOTALL)
tr_match = re.search(r'"tr"\s*:\s*\{(.*)\n\s*\};', content, re.DOTALL)

en_block = en_match.group(1) if en_match else ""
tr_block = tr_match.group(1) if tr_match else ""

keys = ['flag-I', 'grave', 'werewolf', 'dolphin', 'flag-II', 'terrain', 'forgetting', 'together']

print("--- EN ---")
for k in keys:
    match = re.search(rf'"{k}"\s*:\s*\{{\s*"title"\s*:\s*"([^"]+)"', en_block)
    if match:
        t = match.group(1)
        clean = t.split(';')[0].split(',')[0].strip()
        print(f"{k}: '{t}' => '{clean}'")
    else:
        print(f"{k}: NOT FOUND")

print("--- TR ---")
for k in keys:
    match = re.search(rf'"{k}"\s*:\s*\{{\s*"title"\s*:\s*"([^"]+)"', tr_block)
    if match:
        t = match.group(1)
        clean = t.split(';')[0].split(',')[0].strip()
        print(f"{k}: '{t}' => '{clean}'")
    else:
        print(f"{k}: NOT FOUND")
