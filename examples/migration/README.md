# Read-only rename example

From the source repository root:

```sh
python3 -B tools/migrate_catalog.py --catalog examples/migration/marketplace-before.json
```

`proposed_catalog` must equal `marketplace-after.json`. Notice that the unrelated plugin,
marketplace label, and the old entry’s restrictive installation policy remain unchanged.
Neither input file is modified. The accompanying TOML is an inert local-disable example,
not permission to edit live settings or an automatically loaded configuration.
