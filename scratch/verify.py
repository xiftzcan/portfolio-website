import os
import re

# Correct newest-to-oldest sequence
sequence = [
    "anayasa-lemmatizer.html",
    "all-together.html",
    "terra-incognita.html",
    "flag-ii.html",
    "perpetual-forgetting.html",
    "bridging-the-gap.html",
    "werewolf-dream.html",
    "flag-as-volatile-form.html",
    "coasts-of-lives.html"
]

projects_dir = "projects"
success = True

print("=== VERIFYING PROJECT NAVIGATION LINKS ===")

for i, filename in enumerate(sequence):
    filepath = os.path.join(projects_dir, filename)
    if not os.path.exists(filepath):
        print(f"[FAIL] File not found: {filepath}")
        success = False
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find prev and next links
    prev_match = re.search(r'class="prev-project"[^>]*href="([^"]+)"', content)
    next_match = re.search(r'class="next-project"[^>]*href="([^"]+)"', content)
    
    # Also find if there is an alternative format where href comes before class
    if not prev_match:
        prev_match = re.search(r'href="([^"]+)"[^>]*class="prev-project"', content)
    if not next_match:
        next_match = re.search(r'href="([^"]+)"[^>]*class="next-project"', content)

    if not prev_match:
        print(f"[FAIL] {filename}: Could not find prev-project link.")
        success = False
        continue
    if not next_match:
        print(f"[FAIL] {filename}: Could not find next-project link.")
        success = False
        continue

    prev_href = prev_match.group(1)
    next_href = next_match.group(1)

    expected_prev = sequence[i - 1]
    expected_next = sequence[(i + 1) % len(sequence)]

    if prev_href != expected_prev:
        print(f"[FAIL] {filename}: Expected prev-project to be '{expected_prev}', got '{prev_href}'")
        success = False
    else:
        print(f"[ OK ] {filename}: Prev points to {prev_href}")

    if next_href != expected_next:
        print(f"[FAIL] {filename}: Expected next-project to be '{expected_next}', got '{next_href}'")
        success = False
    else:
        print(f"[ OK ] {filename}: Next points to {next_href}")

if success:
    print("\n[SUCCESS] All project navigation links form a correct circular sequence!")
else:
    print("\n[FAILURE] One or more project navigation links are incorrect.")
    exit(1)
