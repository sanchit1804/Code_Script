import os
import subprocess

# To Ignore certain folders
IGNORE_DIRS = {'.git', '.github', '__pycache__', 'node_modules'}
ROOT_DIR = os.getcwd()
INDEX_FILE = os.path.join(ROOT_DIR, "INDEX.md")

# Emojis per language
LANG_EMOJIS = {
    "Python": "🐍",
    "JavaScript": "🟨",
    "Java": "☕",
    "C++": "💻",
    "Go": "🌐",
    "WebDev": "🎨",
    "Others": "📁"
}


def get_git_author(project_path):
    """Return the first Git author who added content in this folder"""
    try:
        # To Get the earliest commit author for this folder
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%an", "--", project_path],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True
        )
        authors = result.stdout.strip().split("\n")
        if authors and authors[0]:
            return f"@{authors[0].replace(' ', '')}"  # This Convert spaces → none
    except Exception:
        pass
    return "@unknown"


def generate_index(root_dir="."):
    content = [
        "# 📘 Code Script Index\n",
        "A central list of all scripts and mini-projects organized by language.\n",
        "---\n\n"
    ]

    for language in sorted(os.listdir(root_dir)):
        lang_path = os.path.join(root_dir, language)
        if not os.path.isdir(lang_path) or language in IGNORE_DIRS or language.startswith('.'):
            continue

        emoji = LANG_EMOJIS.get(language, "📂")
        content.append(f"## {emoji} {language}\n\n")
        content.append("| Project | Author |\n")
        content.append("|----------|---------|\n")

        added_any = False
        for project in sorted(os.listdir(lang_path)):
            project_path = os.path.join(lang_path, project)
            if not os.path.isdir(project_path):
                continue

            author = get_git_author(project_path)
            content.append(f"| {project} | {author} |\n")
            added_any = True

        if not added_any:
            content.append("| _No projects yet_ | - |\n")

        content.append("\n")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.writelines(content)

    print("✅ INDEX.md has been successfully generated using Git commit authors!")


if __name__ == "__main__":
    generate_index()
