import re

with open('assets/js/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find "en": { and match until its closing brace or "tr": {
en_match = re.search(r'"en"\s*:\s*\{(.*)\n\s*"tr"\s*:\s*\{', content, re.DOTALL)
if en_match:
    en_block = en_match.group(1)
    # Find all first-level keys inside the en block
    # These keys are directly indented or followed by :
    keys = re.findall(r'^\s*"([^"]+)"\s*:', en_block, re.MULTILINE)
    print("EN Keys:", keys)
else:
    print("EN block not found")

# Let's find "tr": {
tr_match = re.search(r'"tr"\s*:\s*\{(.*)\n\s*\};', content, re.DOTALL)
if tr_match:
    tr_block = tr_match.group(1)
    keys = re.findall(r'^\s*"([^"]+)"\s*:', tr_block, re.MULTILINE)
    print("TR Keys:", keys)
else:
    print("TR block not found")
