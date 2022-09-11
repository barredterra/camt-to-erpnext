## Code Quality

This project uses `isort` and `black` to format python code.

## Release

Bump version:

```
poetry version [patch | minor | major | prepatch | preminor | premajor | prerelease]
```

Commit bumped version:

```
git add pyproject.toml
git commit -m "chore: bump version"
```

Build package:

```
poetry build
```

Create a GitHub release:

```
gh release create v$(poetry version -s) \
    dist/camt_to_erpnext-$(poetry version -s)-py3-none-any.whl \
    dist/camt-to-erpnext-$(poetry version -s).tar.gz \
    --generate-notes
```

Publish to PyPI:

```
poetry publish
```
