# KbPM
Knowledge-based Package Manager for a start

## Usage

```bash
Packages.py working_dir
```

_working_dir_ is the directory to contain all GitHub repositories (packages).

Uncomment `packages.update_projects()` will trigger the git command.

If source URL is not available, one solution is to copy *.src.jar and uncompress it
under _working_dir_. See `def get_latest_version_packages(...)` in `Packages`.

