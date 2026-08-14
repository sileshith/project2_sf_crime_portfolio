# Data provenance

The project uses the City and County of San Francisco's **Police Department Incident
Reports: 2018 to Present** dataset, DataSF identifier `wg3w-h783`.

The incident-level source is not committed because of its size. The small aggregate
Parquet artifacts under `data/processed/` are committed so the dashboard works from a
clean clone.

Rebuild the aggregates from DataSF:

```bash
uv run sf-incidents-build
uv run sf-incidents-evaluate
```

For a previously downloaded CSV or Parquet source:

```bash
uv run sf-incidents-build --source path/to/incidents.csv
uv run sf-incidents-evaluate
```

`metadata.json` records the source, generation time, row count, and SHA-256 hash for
each dashboard artifact. The data describes reported and recorded incidents; it is not
an estimate of unreported crime or personal risk.

