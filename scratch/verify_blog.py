import os
import re

# Expected sequence (newest-to-oldest)
sequence = [
    "poem/her_eksik_siir_gibi.html",
    "poem/yegane_siir.html",
    "essay/form-violence.html",
    "essay/subversive-classification-cracks.html",
    "essay/ontological-object-gravity.html",
    "essay/relationality-illusion.html",
    "poem/ufuklar_ve_yarinlar.html",
    "poem/kapici_gozlemi.html",
    "poem/doktor_tavsiyesi.html",
    "poem/yokus.html",
    "poem/duragan.html"
]

blog_dir = "blog"
success = True

print("=== VERIFYING BLOG.HTML LISTING ===")
with open("blog.html", "r", encoding="utf-8") as f:
    blog_html = f.read()

# Extract all links inside blog-list container
blog_list_match = re.search(r'(?s)<div class="blog-list">(.*?)</div>\s*(?:</div>|\s*<!-- Pagination -->)', blog_html)
if not blog_list_match:
    print("[FAIL] Could not find blog-list container in blog.html")
    success = False
else:
    blog_list_content = blog_list_match.group(1)
    # Find all hrefs inside h2 elements
    found_hrefs = re.findall(r'<h2><a href="blog/([^"]+)"', blog_list_content)
    
    if len(found_hrefs) != len(sequence):
        print(f"[FAIL] Expected {len(sequence)} posts in blog.html, but found {len(found_hrefs)}: {found_hrefs}")
        success = False
    else:
        mismatch = False
        for idx, href in enumerate(found_hrefs):
            expected = sequence[idx]
            if href != expected:
                print(f"[FAIL] Pos {idx}: Expected '{expected}', got '{href}'")
                success = False
                mismatch = True
        if not mismatch:
            print(f"[ OK ] blog.html contains exactly the {len(sequence)} valid posts in correct chronological order!")

print("\n=== VERIFYING POST NAVIGATION & NEWSLETTER ABSENCE ===")

for i, subpath in enumerate(sequence):
    filepath = os.path.join(blog_dir, subpath)
    if not os.path.exists(filepath):
        print(f"[FAIL] File not found: {filepath}")
        success = False
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify newsletter absence
    if '<div class="newsletter">' in content:
        print(f"[FAIL] {subpath}: newsletter div is still present!")
        success = False
    else:
        print(f"[ OK ] {subpath}: newsletter div is absent")

    # Verify prev and next links
    prev_match = re.search(r'class="prev-post"[^>]*href="([^"]+)"', content)
    next_match = re.search(r'class="next-post"[^>]*href="([^"]+)"', content)
    
    if not prev_match:
        prev_match = re.search(r'href="([^"]+)"[^>]*class="prev-post"', content)
    if not next_match:
        next_match = re.search(r'href="([^"]+)"[^>]*class="next-post"', content)

    if not prev_match:
        print(f"[FAIL] {subpath}: Could not find prev-post link.")
        success = False
        continue
    if not next_match:
        print(f"[FAIL] {subpath}: Could not find next-post link.")
        success = False
        continue

    prev_href = prev_match.group(1)
    next_href = next_match.group(1)

    # Calculate expected hrefs relative to the current file's dir
    from_dir = os.path.dirname(subpath)
    
    expected_prev_subpath = sequence[i - 1]
    expected_next_subpath = sequence[(i + 1) % len(sequence)]
    
    expected_prev_href = os.path.basename(expected_prev_subpath) if os.path.dirname(expected_prev_subpath) == from_dir else f"../{expected_prev_subpath}"
    expected_next_href = os.path.basename(expected_next_subpath) if os.path.dirname(expected_next_subpath) == from_dir else f"../{expected_next_subpath}"

    if prev_href != expected_prev_href:
        print(f"[FAIL] {subpath}: Expected prev-post href to be '{expected_prev_href}', got '{prev_href}'")
        success = False
    else:
        print(f"[ OK ] {subpath}: Prev points correctly to {prev_href}")

    if next_href != expected_next_href:
        print(f"[FAIL] {subpath}: Expected next-post href to be '{expected_next_href}', got '{next_href}'")
        success = False
    else:
        print(f"[ OK ] {subpath}: Next points correctly to {next_href}")

# Check templates for newsletter absence
templates = [
    "essay/essay_template.html",
    "poem/poem_template.html",
    "reflection/reflection_template.html",
    "research/research_template.html"
]
print("\n=== VERIFYING TEMPLATES ===")
for temp in templates:
    filepath = os.path.join(blog_dir, temp)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if '<div class="newsletter">' in content:
            print(f"[FAIL] Template {temp}: newsletter div is still present!")
            success = False
        else:
            print(f"[ OK ] Template {temp}: newsletter div is absent")

if success:
    print("\n[SUCCESS] All checks passed successfully!")
else:
    print("\n[FAILURE] Validation failed.")
    exit(1)
