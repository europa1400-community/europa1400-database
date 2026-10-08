# 📚 Europa 1400 Database

Which versions of **Europa 1400: The Guild** (*Die Gilde*) exist, and which community patches and fixes fit them.

**Players:** you do not need anything from here. The
[Europa 1400 Manager](https://github.com/europa1400-community/europa1400-manager) reads this database and installs the
right patches for your game. To look things up, browse the website:
**[europa1400-community.github.io/europa1400-database](https://europa1400-community.github.io/europa1400-database/)**

---

## What is in here

YAML tables in [`data/`](data/):

| Table | Content |
|---|---|
| `edition.yml`, `version.yml`, `language.yml`, `distribution.yml`, `drm.yml` | editions, versions, languages, distributions (GOG, Steam, CD), copy protection |
| `executable.yml`, `executable_to_metadata.yml` | game executables and which version they belong to |
| `patch.yml` | third-party patches (DDrawCompat, DXVK, dxwrapper, ...) |
| `e1400patch.yml` | patch loader and patches of [europa1400-patches](https://github.com/europa1400-community/europa1400-patches) (manager 1.2 or newer) |
| `metadata_to_patch.yml` | which patch fits which game version |

The manager downloads the tables from the `master` branch, so a merged change reaches every player at the next start.
Older managers fail on patch types they do not know: new patch types go into a table of their own (like
`e1400patch.yml`), not into `patch.yml`.

## Contributing

1. Edit the YAML in `data/` (ids are lowercase, unique within a table).
2. Preview the website: `uv sync --group docs` and `uv run mkdocs serve`.
3. Open a pull request with a [Conventional Commits](https://www.conventionalcommits.org/) title (`feat: add ...`).

The website is built and published by GitHub Actions on every push to `master`.
