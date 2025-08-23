from pathlib import Path

import yaml
from mkdocs_gen_files import open as open_gen_file


def generate_tables():
    data_dir = Path("data")
    output_dir = Path("tables")

    # For navigation structure
    nav_lines = []
    index_lines = [
        "# Tables Overview",
        "",
        "This section contains all available data tables for Europa 1400.",
        "",
        "## Available Tables",
        "",
    ]

    for path in sorted(data_dir.glob("*.yml")):
        name = path.stem
        with path.open("r", encoding="utf-8") as f:
            table = yaml.safe_load(f)

        title = table.get("name", name.replace("_", " ").title())
        elements = table.get("elements", [])

        # Markdown table content
        lines = [f"# {title}", ""]
        if not elements:
            lines.append("_No elements defined._")
        else:
            headers = sorted({k for el in elements for k in el})
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("|" + "|".join("---" for _ in headers) + "|")
            for el in elements:
                row = [str(el.get(h, "")) for h in headers]
                lines.append("| " + " | ".join(row) + " |")

        md_file = f"{name}.md"
        md_path = output_dir / md_file

        with open_gen_file(md_path, "w") as f:
            f.write("\n".join(lines) + "\n")
            # Note: set_edit_path is not used here as the generated files
            # are processed by literate-nav and don't exist as separate entities

        # For nav
        nav_lines.append(f"    - {title}: tables/{md_file}")
        # For tables/index.md
        index_lines.append(f"- [{title}]({md_file})")

    # Write tables/index.md
    with open_gen_file("tables/index.md", "w") as f:
        f.write("\n".join(index_lines) + "\n")

    return nav_lines


# Generate tables and return nav lines for potential future use
tables_nav = generate_tables()

# Note: Navigation is now handled directly in generate_summary.py
# The pickle file approach has been removed to avoid dependency issues
