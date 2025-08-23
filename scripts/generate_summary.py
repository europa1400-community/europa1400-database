from pathlib import Path

from mkdocs_gen_files import open as open_gen_file


def extract_title_from_markdown(file_path):
    """Extract the title from a markdown file, looking for the first # heading."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

        import re

        # Look for the first # heading
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fallback to filename if no title found
        return file_path.stem.replace("_", " ").replace("-", " ").title()
    except Exception:
        # Fallback to filename if file can't be read
        return file_path.stem.replace("_", " ").replace("-", " ").title()


def generate_summary():
    """Generate the main SUMMARY.md file for literate-nav"""

    # Initialize navigation structure using explicit links
    nav_lines = [
        "- [Home](index.md)",
        "- [Articles](articles/index.md)",
    ]

    # Generate articles navigation
    articles_dir = Path("docs/articles")
    if articles_dir.exists():
        for md_file in sorted(articles_dir.glob("*.md")):
            if md_file.name != "index.md":
                title = extract_title_from_markdown(md_file)
                nav_lines.append(f"    - [{title}](articles/{md_file.name})")

    # Add tables section using wildcard pattern that literate-nav loves
    nav_lines.append("- [Tables](tables/index.md)")
    nav_lines.append("    - tables/*.md")

    # Write the SUMMARY.md file
    with open_gen_file("SUMMARY.md", "w") as f:
        f.write("\n".join(nav_lines) + "\n")


# Generate the main navigation
generate_summary()
