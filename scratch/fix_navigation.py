import os
import re

# Newest-to-oldest project sequence
sequence = [
    ("anayasa-lemmatizer.html", "Turkish Constitution Lemmatizer"),
    ("all-together.html", "All Together"),
    ("terra-incognita.html", "Terra Incognita"),
    ("flag-ii.html", "Flag II (Untitled)"),
    ("perpetual-forgetting.html", "Perpetual Forgetting"),
    ("bridging-the-gap.html", "Bridging the Gap"),
    ("werewolf-dream.html", "Werewolf Dream"),
    ("flag-as-volatile-form.html", "Flag as a Volatile Form"),
    ("coasts-of-lives.html", "Coasts of Lives")
]

projects_dir = "projects"

for i, (filename, title) in enumerate(sequence):
    filepath = os.path.join(projects_dir, filename)
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.")
        continue
    
    # Neighbors (circular)
    prev_filename, prev_title = sequence[i - 1]
    next_filename, next_title = sequence[(i + 1) % len(sequence)]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Locate project-navigation block and its indentation
    # Matching any spacing, but we'll extract the trailing line spaces specifically
    pattern = r'(?s)(\n[ \t]*)<div class="project-navigation">.*?</div>'
    
    def make_replacement(match):
        indent = match.group(1).replace('\n', '')
        replacement = (
            f"\n{indent}<div class=\"project-navigation\">\n"
            f"{indent}    <a href=\"{prev_filename}\" class=\"prev-project\">\n"
            f"{indent}        <span class=\"nav-arrow\">←</span>\n"
            f"{indent}        <span class=\"nav-title\">{prev_title}</span>\n"
            f"{indent}    </a>\n"
            f"{indent}    <a href=\"../works.html\" class=\"all-projects\" data-translate=\"allWorks\">All Works</a>\n"
            f"{indent}    <a href=\"{next_filename}\" class=\"next-project\">\n"
            f"{indent}        <span class=\"nav-title\">{next_title}</span>\n"
            f"{indent}        <span class=\"nav-arrow\">→</span>\n"
            f"{indent}    </a>\n"
            f"{indent}</div>"
        )
        return replacement

    new_content, count = re.subn(pattern, make_replacement, content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully cleaned and updated navigation in {filename}.")
    else:
        print(f"Warning: project-navigation div not found in {filename}.")
