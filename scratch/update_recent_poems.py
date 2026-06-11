import os
import re

poem_dir = "blog/poem"
new_sidebar = """            <div class="popular-posts">
                <h3>Recent Poems</h3>
                <ul>
                    <li>
                        <a href="her_eksik_siir_gibi.html">Her Eksik Şiir Gibi</a>
                        <span class="post-date">June 11, 2026</span>
                    </li>
                    <li>
                        <a href="yegane_siir.html">Yegane Şiir</a>
                        <span class="post-date">June 11, 2026</span>
                    </li>
                    <li>
                        <a href="ufuklar_ve_yarinlar.html">Ufuklar ve Yarınlar</a>
                        <span class="post-date">May 24, 2025</span>
                    </li>
                    <li>
                        <a href="kapici_gozlemi.html">Kapıcı Gözlemi</a>
                        <span class="post-date">August 04, 2020</span>
                    </li>
                </ul>
            </div>"""

pattern = r'(?s)([ \t]*)<div class="popular-posts">.*?</div>'

for root, dirs, files in os.walk(poem_dir):
    for file in files:
        if not file.endswith(".html"):
            continue
        # Skip her_eksik_siir_gibi since it already has it
        if file == "her_eksik_siir_gibi.html":
            continue
            
        filepath = os.path.join(root, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content, count = re.subn(pattern, lambda m: m.group(1) + new_sidebar.strip(), content)
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated Recent Poems sidebar in {file}")
        else:
            print(f"Warning: popular-posts sidebar not found in {file}")

print("Done updating sidebars!")
