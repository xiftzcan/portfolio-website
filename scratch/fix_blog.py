import os
import re

# Sorted newest-to-oldest sequence of active blog posts (with titles and translation keys if they exist)
posts = [
    ("essay/form-violence.html", "The Violence of Form", "formViolence"),
    ("essay/subversive-classification-cracks.html", "Classification as a Subversive Methodology and the Exposure of Cracks", "subversiveClassification"),
    ("essay/ontological-object-gravity.html", "The Ontological Transformation of the Object and Specific Gravity", "objectGravity"),
    ("essay/relationality-illusion.html", "The Illusion and Dilemma of Relationality: The Rejection of Micro-Utopias", "relationality"),
    ("poem/ufuklar_ve_yarinlar.html", "Ufuklar ve Yarınlar", None),
    ("essay/digital-memory-blog.html", "Digital Memory and Algorithmic Art", None),
    ("poem/kapici_gozlemi.html", "Kapıcı Gözlemi", None),
    ("poem/suslu_bir_siir.html", "Süslü Bir Şiir", None),
    ("poem/yokus.html", "Yokuş", None),
    ("poem/duragan.html", "Durağan", None)
]

blog_dir = "blog"

# 1. Delete legacy blog/digital-memory-blog.html if it exists
legacy_file = os.path.join(blog_dir, "digital-memory-blog.html")
if os.path.exists(legacy_file):
    os.remove(legacy_file)
    print("Deleted legacy blog/digital-memory-blog.html")

# Helper to calculate relative path between two subpaths (e.g. 'essay/a.html' and 'poem/b.html')
def get_relative_href(from_subpath, to_subpath):
    from_dir = os.path.dirname(from_subpath)
    to_dir = os.path.dirname(to_subpath)
    to_file = os.path.basename(to_subpath)
    if from_dir == to_dir:
        return to_file
    else:
        return f"../{to_subpath}"

# 2 & 3. Process all HTML files recursively for newsletter removal and active files for navigation update
for root, dirs, files in os.walk(blog_dir):
    for file in files:
        if not file.endswith(".html"):
            continue
        
        filepath = os.path.join(root, file)
        # Calculate subpath relative to blog_dir (e.g., 'essay/form-violence.html')
        subpath = os.path.relpath(filepath, blog_dir).replace("\\", "/")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # Remove newsletter block (including its preceding spacing/indentation)
        newsletter_pattern = r'(?s)(\s*)<div class="newsletter">.*?</div>'
        content, count = re.subn(newsletter_pattern, "", content)
        if count > 0:
            print(f"Removed newsletter div from {subpath}")
            modified = True
            
        # Update navigation block if it is one of the active blog posts
        matching_post_index = next((idx for idx, p in enumerate(posts) if p[0] == subpath), None)
        if matching_post_index is not None:
            # Determine circular neighbors
            prev_subpath, prev_title, prev_key = posts[matching_post_index - 1]
            next_subpath, next_title, next_key = posts[(matching_post_index + 1) % len(posts)]
            
            prev_href = get_relative_href(subpath, prev_subpath)
            next_href = get_relative_href(subpath, next_subpath)
            
            prev_translate_attr = f' data-translate="{prev_key}.title"' if prev_key else ''
            next_translate_attr = f' data-translate="{next_key}.title"' if next_key else ''
            
            nav_pattern = r'(?s)(\n[ \t]*)<div class="post-navigation">.*?</div>'
            
            def make_nav_replacement(match):
                indent = match.group(1).replace('\n', '')
                replacement = (
                    f"\n{indent}<div class=\"post-navigation\">\n"
                    f"{indent}    <a href=\"{prev_href}\" class=\"prev-post\">\n"
                    f"{indent}        <span class=\"nav-arrow\">←</span>\n"
                    f"{indent}        <span class=\"nav-title\"{prev_translate_attr}>{prev_title}</span>\n"
                    f"{indent}    </a>\n"
                    f"{indent}    <a href=\"../../blog.html\" class=\"all-posts\">All Posts</a>\n"
                    f"{indent}    <a href=\"{next_href}\" class=\"next-post\">\n"
                    f"{indent}        <span class=\"nav-title\"{next_translate_attr}>{next_title}</span>\n"
                    f"{indent}        <span class=\"nav-arrow\">→</span>\n"
                    f"{indent}    </a>\n"
                    f"{indent}</div>"
                )
                return replacement
            
            content, nav_count = re.subn(nav_pattern, make_nav_replacement, content)
            if nav_count > 0:
                print(f"Updated navigation in {subpath}")
                modified = True
            else:
                print(f"Warning: post-navigation block not found in active post: {subpath}")
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
