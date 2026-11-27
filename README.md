# CI Reliability Analytics

Where does GitHub Actions CI lose time, and can we measure the effect of a specific improvement?

This project will collect GitHub Actions run, attempt, and job metadata, model it with Python, DuckDB, and dbt, and surface reliability and latency metrics in Power BI. A controlled experiment will test an improvement on a selected workflow.

## Status

The project is starting with a data source pilot. The pilot will compare public repositories for data coverage and reproducibility, then select workflows for analysis.

## First release

Version 0.1 will reproduce the local pipeline from a checked-in sample with one command. CI will run the same path. A Power BI Import report will open offline, and selected metrics will be checked against SQL.

See the [issues](https://github.com/DanR-ghub/ci-reliability-analytics/issues) and [milestones](https://github.com/DanR-ghub/ci-reliability-analytics/milestones) for work in progress and acceptance criteria.
