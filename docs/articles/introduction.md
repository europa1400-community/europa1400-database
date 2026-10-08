# Introduction

The database describes the game in small tables that reference each other by id:

- **Game metadata**: edition (Standard, Gold), version (v1.01 ... v2.06), language, distribution (GOG, Steam, CD) and
  copy protection. The manager identifies the installed game by its executable (`executable.yml`,
  `executable_to_metadata.yml`).
- **Patches**: third-party fixes in `patch.yml`, the patch loader and its patches in `e1400patch.yml`. Each entry has a
  download URL and a type that tells the manager how to install it.
- **Mappings**: `metadata_to_patch.yml` lists which patch fits which game version.

To add or correct something, edit the YAML files in the
[repository](https://github.com/europa1400-community/europa1400-database) and open a pull request.
