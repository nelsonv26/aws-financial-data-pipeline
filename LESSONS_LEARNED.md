# Lessons Learned — AWS Financial Data Pipeline

> Last updated: May 2026

---

## 📌 Context

End-to-end cloud data pipeline built as a portfolio project. Covers Python ETL, AWS S3 + Athena, dbt transformations, Terraform IaC, GitHub Actions CI/CD, and Apache Superset for visualization. Dataset: daily financial market + macroeconomic data for S&P 500, NASDAQ, and Dow Jones from 2000 to 2008.

---

## ✅ What Worked Well

- **Hive-style partitioning from day one.** Structuring S3 data as `year=YYYY/` made Athena partition pruning work automatically without any extra configuration. Athena reads only the partitions it needs, which keeps query costs low on a dataset spanning 8+ years.

- **Separating CSV partitions from Parquet partitions.** Having two output formats (`processed_partitioned/` for CSV and `processed_parquet/` for Athena) turned out to be useful — CSV made it easy to inspect and debug individual year slices, while Parquet is what actually powers the queries. Running both in the pipeline added minimal cost.

- **dbt layering (staging → mart) even for a small project.** It was tempting to write a single fat model. Keeping a clean staging layer (`stg_financial_data`) with type casting separated from the aggregation mart meant that adding new mart models later required zero changes to the staging layer. Good discipline even at this scale.

- **Terraform for S3 + Athena setup.** Provisioning these two resources with Terraform added very little overhead and made the entire infrastructure reproducible from scratch. No more "I created that bucket manually months ago and forgot the settings."

- **Custom Superset Dockerfile with PyAthena.** Installing `pyathena[pandas]` inside Superset's existing venv (via `. /app/.venv/bin/activate && uv pip install`) was the correct approach. Trying to install at the OS level first caused silent failures because Superset doesn't see packages outside its venv.

---

## ❌ What Didn't Work / Mistakes Made

- **`stg_financial_data.yml` declares a second `sources` block that conflicts with `sources.yml`.** The staging model YAML file has both a `sources:` key (which should only live in `sources.yml`) and a `models:` key in the same file. This causes dbt to see duplicate source definitions. The `sources:` block inside `stg_financial_data.yml` references a different table name (`processed_finance_partitioned`) than the one in `sources.yml` (`processed_finance_parquet`), which would cause the dbt run to fail or silently query the wrong table.

- **`stg_financial_data.sql` references fields that don't exist in the source.** The model selects `high_price` and `low_price`, but the raw dataset columns after cleaning are `daily_high` and `daily_low`. This would throw an Athena column-not-found error at runtime. The cleaning script renames columns correctly, but the dbt model wasn't updated to match.

- **The Superset `docker-compose.yml` hardcodes a Windows absolute path.** The volume mount `C:\Users\nelso\.aws:/root/.aws` works locally on Windows but immediately breaks if anyone else runs the project, or if it's ever deployed to Linux. AWS credentials should be passed as environment variables or handled via IAM roles, not bind-mounted from a host path.

- **`run_pipeline.py` uses a different S3 bucket name than Terraform and dbt.** The pipeline script uploads to `nelson-aws-financial-data-lake`, but the Terraform config creates `nelson-financial-data-lake-001` and dbt's profiles use `s3://nelson-financial-data-lake-001/`. Three different names for what should be one bucket. Uploads in the script would silently succeed (if the second bucket happened to exist) but dbt would query the wrong location.

- **No `LESSONS_LEARNED.md` or architecture docs at project start.** Decisions like "why two partition formats?" and "why Athena over Redshift?" were never written down during build. Having to reconstruct intent from code alone is slower and less accurate.

---

## 🔁 What I'd Do Differently

- **Define a single source-of-truth for the bucket name** — one variable in Terraform output, referenced in a `.env` file that both the Python scripts and dbt profiles read. Never hardcode the bucket name in three places.

- **Fix the `stg_financial_data.yml` source duplication immediately.** Move all source declarations to `sources.yml` only, and have the model YAML contain only the `models:` block. This is the dbt convention and avoiding it causes silent bugs.

- **Use column aliases in `stg_financial_data.sql` to match the actual source schema** (`daily_high as high_price`, `daily_low as low_price`) — or rename the columns in the Python cleaning step to match what dbt expects. Pick one direction and be consistent.

- **Replace the hardcoded Windows path in `docker-compose.yml`** with `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` env vars already declared in the `environment:` block — they're already there, just not used for auth. Remove the volume mount entirely.

- **Add a `mart_macro_indicators` model from the start.** The raw data has GDP growth, inflation, interest rates, oil prices, and gold prices per day — all unused in the current mart. This is the most analytically interesting part of the dataset and building it early would have driven more interesting Superset dashboards.

- **Use `dbt docs generate` in the GitHub Actions workflow.** Adding one step to publish dbt lineage docs (even just as a workflow artifact) would make the project significantly more impressive as a portfolio piece.

---

## 💡 Key Technical Insights

1. **Athena requires `MSCK REPAIR TABLE` or explicit partition registration after new S3 uploads.** Simply uploading new `year=YYYY/` folders to S3 doesn't automatically make Athena aware of them. Either run `MSCK REPAIR TABLE` in Athena after each upload, or use `aws glue create-partition` to register them programmatically. This is a common gotcha when first using Athena with Hive partitioning.

2. **`dbt-athena-community` requires `s3_staging_dir` to end with a trailing slash.** Without it, Athena query results get written to unexpected paths and the connector raises a hard-to-diagnose error. The profile in this project has it correctly set to `s3://nelson-financial-data-lake-001/` but it's easy to forget when setting up a new environment.

3. **PyAthena inside Superset must be installed in Superset's own virtualenv, not at the system level.** Superset runs inside a Python venv at `/app/.venv`. Standard `pip install` at the Dockerfile `RUN` level installs into the system Python, which Superset never sees. The fix is to activate the venv first: `. /app/.venv/bin/activate && uv pip install pyathena[pandas]`.

4. **`year()` is valid Athena SQL but not standard SQL.** The mart model uses `year(date)` to extract the year — this works in Athena (Trino/Presto dialect) but would break if the target was ever switched to PostgreSQL or BigQuery. Prefer `EXTRACT(YEAR FROM date)` for portability.

5. **`boto3.client("s3").upload_file` doesn't create the bucket if it doesn't exist.** It raises a `NoSuchBucket` error. Always provision S3 with Terraform (or create manually) before running the upload script. There's no guard in `upload_to_s3.py` for this.

6. **GitHub Actions `working-directory` only applies to the step it's set on.** Each dbt step (`dbt deps`, `dbt run`, `dbt test`) has `working-directory: financial_dbt` set correctly. If any step is added without this, dbt won't find `dbt_project.yml` and will fail with a confusing "not a dbt project" error.

---

## 🧱 Technical Debt & Open Issues

- **Bucket name inconsistency across three files** (`run_pipeline.py`, `terraform/s3.tf`, `.github/workflows/dbt_pipeline.yml`) — needs a single `.env` or Terraform output to unify them.
- **Duplicate source declaration in `stg_financial_data.yml`** — will cause `dbt compile` warnings and potential runtime failures.
- **Column name mismatch** in `stg_financial_data.sql` (`high_price`/`low_price` vs actual `daily_high`/`daily_low`).
- **No `dbt test` coverage for numeric validity** — `not_null` tests exist but there's no check that prices are positive or trading volume is non-negative.
- **No `.env.example` file** — a contributor has no template for the required environment variables.
- **Airflow DAG paths are hardcoded** to `/opt/airflow/dbt` — would need adjustment for any real deployment.
- **No data freshness check** — Airflow runs daily but there's no alert if the S3 data hasn't been updated.

---

## 📚 References That Helped

- [dbt-athena-community docs](https://github.com/dbt-athena/dbt-athena) — especially the profiles.yml setup and known Athena SQL dialect quirks
- [Athena partitioning guide (AWS docs)](https://docs.aws.amazon.com/athena/latest/ug/partitions.html) — for understanding MSCK REPAIR TABLE behavior
- [PyAthena SQLAlchemy connection strings](https://github.com/laughingman7743/PyAthena#sqlalchemy) — for the Superset database connection URI format
- [Apache Superset custom Docker images](https://superset.apache.org/docs/installation/docker-compose/) — for understanding the venv structure and why system-level pip installs don't work
