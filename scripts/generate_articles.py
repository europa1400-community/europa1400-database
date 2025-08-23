import re
from pathlib import Path

from mkdocs_gen_files import open as open_gen_file


def extract_title_from_markdown(file_path):
    """Extract the title from a markdown file, looking for the first # heading."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Look for the first # heading
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fallback to filename if no title found
        return file_path.stem.replace("_", " ").replace("-", " ").title()
    except Exception:
        # Fallback to filename if file can't be read
        return file_path.stem.replace("_", " ").replace("-", " ").title()


def extract_description_from_markdown(file_path, max_length=150):
    """Extract a brief description from the markdown content."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Remove the title line
        content = re.sub(r"^# .+$", "", content, count=1, flags=re.MULTILINE)

        # Remove other markdown formatting
        content = re.sub(r"#{1,6}\s+", "", content)  # Remove headers
        content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)  # Remove bold
        content = re.sub(r"\*(.+?)\*", r"\1", content)  # Remove italic
        content = re.sub(r"`(.+?)`", r"\1", content)  # Remove code
        content = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", content)  # Remove links

        # Get first paragraph
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        if paragraphs:
            description = paragraphs[0]
            if len(description) > max_length:
                description = description[:max_length].rsplit(" ", 1)[0] + "..."
            return description

        return "No description available."
    except Exception:
        return "No description available."


def generate_articles():
    articles_dir = Path("docs/articles")
    output_path = Path("articles/index.md")
    nav_lines = []

    # Generate articles index
    index_lines = [
        "# Articles",
        "",
        "Welcome to the Europa 1400 articles section. Here you'll find detailed guides, explanations, and documentation about various aspects of the game.",
        "",
        "## Available Articles",
        "",
    ]

    if not articles_dir.exists():
        index_lines.append("_No articles available yet._")
    else:
        # Find all markdown files in the articles directory
        article_files = []

        # Collect all .md files
        for md_file in articles_dir.glob("*.md"):
            if md_file.name != "index.md":  # Skip index files
                title = extract_title_from_markdown(md_file)
                description = extract_description_from_markdown(md_file)
                relative_path = md_file.name

                # Copy the article content to the generated articles folder
                with md_file.open("r", encoding="utf-8") as f:
                    article_content = f.read()

                with open_gen_file(f"articles/{relative_path}", "w") as f:
                    f.write(article_content)
                    # Note: set_edit_path is not used here as the generated files
                    # are processed by literate-nav and don't exist as separate entities

                article_files.append(
                    {
                        "title": title,
                        "description": description,
                        "path": relative_path,
                        "file": md_file,
                    }
                )

                # Add to navigation
                nav_lines.append(f"    - {title}: articles/{relative_path}")

        # Sort articles by title
        article_files.sort(key=lambda x: x["title"].lower())

        if not article_files:
            index_lines.append("_No articles available yet._")
        else:
            for article in article_files:
                index_lines.append(f"- [{article['title']}]({article['path']})")

    # Write the articles index file
    with open_gen_file(output_path, "w") as f:
        f.write("\n".join(index_lines) + "\n")
        # Note: set_edit_path is not used here as the generated files
        # are processed by literate-nav and don't exist as separate entities

    return nav_lines


# Generate articles and return nav lines for potential future use
articles_nav = generate_articles()

# Note: Navigation is now handled directly in generate_summary.py
# The pickle file approach has been removed to avoid dependency issues
