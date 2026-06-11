import os
import re

# Remaining active blog posts in chronological order (newest-to-oldest)
posts = [
    ("poem/her_eksik_siir_gibi.html", "Her Eksik Şiir Gibi", None),
    ("poem/yegane_siir.html", "Yegane Şiir", None),
    ("essay/form-violence.html", "The Violence of Form", "formViolence"),
    ("essay/subversive-classification-cracks.html", "Classification as a Subversive Methodology and the Exposure of Cracks", "subversiveClassification"),
    ("essay/ontological-object-gravity.html", "The Ontological Transformation of the Object and Specific Gravity", "objectGravity"),
    ("essay/relationality-illusion.html", "The Illusion and Dilemma of Relationality: The Rejection of Micro-Utopias", "relationality"),
    ("poem/ufuklar_ve_yarinlar.html", "Ufuklar ve Yarınlar", None),
    ("poem/kapici_gozlemi.html", "Kapıcı Gözlemi", None),
    ("poem/doktor_tavsiyesi.html", "Doktor Tavsiyesi", None),
    ("poem/yokus.html", "Yokuş", None),
    ("poem/duragan.html", "Durağan", None)
]

blog_dir = "blog"

# 1. Remove Digital Memory post from blog.html
blog_html_path = "blog.html"
if os.path.exists(blog_html_path):
    with open(blog_html_path, "r", encoding="utf-8") as f:
        blog_html = f.read()

    # Regex to match the entire blog-post block for Digital Memory
    post_pattern = r'(?s)[ \t]*<!-- Post: Digital Memory and Algorithmic Art -->\s*<div class="blog-post"[^>]*>.*?</div>\s*'
    new_blog_html, count = re.subn(post_pattern, "", blog_html)
    if count > 0:
        with open(blog_html_path, "w", encoding="utf-8") as f:
            f.write(new_blog_html)
        print(f"Removed Digital Memory post from blog.html ({count} replacement)")
    else:
        print("Warning: Could not find Digital Memory post in blog.html")

# 2. Delete the physical file blog/essay/digital-memory-blog.html
file_to_delete = os.path.join(blog_dir, "essay/digital-memory-blog.html")
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted {file_to_delete}")
else:
    print(f"File {file_to_delete} does not exist on disk")

# Helper to calculate relative path between two subpaths
def get_relative_href(from_subpath, to_subpath):
    from_dir = os.path.dirname(from_subpath)
    to_dir = os.path.dirname(to_subpath)
    to_file = os.path.basename(to_subpath)
    if from_dir == to_dir:
        return to_file
    else:
        return f"../{to_subpath}"

# 3. Process all remaining active posts to update their circular navigation
for root, dirs, files in os.walk(blog_dir):
    for file in files:
        if not file.endswith(".html"):
            continue
        
        filepath = os.path.join(root, file)
        # Calculate subpath relative to blog_dir
        subpath = os.path.relpath(filepath, blog_dir).replace("\\", "/")
        
        # Check if this is one of our active 9 posts
        matching_post_index = next((idx for idx, p in enumerate(posts) if p[0] == subpath), None)
        if matching_post_index is not None:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
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
            
            new_content, nav_count = re.subn(nav_pattern, make_nav_replacement, content)
            if nav_count > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated navigation in {subpath}")
            else:
                print(f"Warning: post-navigation block not found in active post: {subpath}")

print("Done fixing blog posts!")
