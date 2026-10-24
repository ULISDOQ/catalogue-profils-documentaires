# GED-04 — metadata-only candidate discovery

This helper is strictly bounded to the authorization
`GED04_PCIA_PHONE_DOWNLOADS_CANDIDATE_DISCOVERY_001`.

It does **not open or read document contents**.

It uses only:

- directory entries;
- file names;
- extensions;
- file sizes;
- extension-based MIME guesses.

It produces two local files:

- `/tmp/ged04-metadata-inventory.json` — full local inventory including relative names;
- `/tmp/ged04-candidate-summary.json` — redacted summary suitable for routing back to ULISDOQ/GED-RÉEL.

No inventory result is committed to Git automatically.

Example:

```bash
python3 metadata_only_inventory.py "/path/to/PHONE_DOWNLOADS_DIRECTORY" --recursive
```

Then return only:

```bash
cat /tmp/ged04-candidate-summary.json
```

unless Jean explicitly authorizes sharing the full local inventory.
