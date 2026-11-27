# Pilot source survey

## Scope and method

Screen 20 public repositories with GitHub Actions CI. The initial eight provide a baseline across general-purpose Python projects, test tooling, packaging, and interpreter CI. The additional twelve include eight data-stack projects and four comparison projects with different test surfaces or workflow structures. This is a purposive sample for source selection.

On November 27, 2026 UTC, query the [repository workflow runs API](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository) with `event=pull_request`, `status=completed`, `created=2026-10-01..2026-11-26`, and `per_page=15`. Dates refer to run creation in UTC. Keep every returned row, including cancelled and skipped runs. The first page is a recent diagnostic sample for each repository. Several first pages cover only one day.

Record the API's `total_count` separately from sampled metrics. Filtered searches have a documented retrieval limit of 1,000 results per search. Treat API totals above that limit as volume signals. Enumerating them requires narrower windows and deduplication by repository and run ID. Counts reflect the query time. Retention, deletions, and late attempts can change later results.

Use the first page to inspect schema, workflow concentration, reruns, and linkage signals. Fifteen rows at repository level cannot support workflow-level tail latency, rerun recovery rates, or a conclusion about missing PR references. For deeper validation, use stable workflow IDs or paths, cover more than one day, check attempt and job completeness, and prefer roughly 200 eligible runs per workflow for the initial comparison. Show the actual denominator per metric and validate linkage independently where PR-level metrics are planned.

For each repository, query `/actions/runs/{run_id}/attempts/1/jobs?per_page=1` for the first sampled run with `run_attempt > 1`, or the first sampled run when no rerun appears. Record the returned job count. A zero means that the requested attempt returned zero jobs. A successful probe establishes endpoint access for that attempt.

## Results

### Initial screening

| Repository | Reported API total | Sampled runs | Sample creation span (UTC) | Workflow paths | Sampled reruns | Sampled runs with PR metadata | Reported jobs in probed first attempt |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `psf/requests` | 30 | 15 | 2026-11-02 – 2026-11-02 | 5 | 0 | 10 | [0](https://github.com/psf/requests/actions/runs/41505615242) |
| `pallets/flask` | 5 | 5 | 2026-10-07 – 2026-10-30 | 3 | 0 | 0 | [1](https://github.com/pallets/flask/actions/runs/41077327237) |
| `psf/black` | 2500 | 15 | 2026-11-26 – 2026-11-26 | 6 | 0 | 0 | [0](https://github.com/psf/black/actions/runs/45891413930) |
| `pypa/packaging` | 1963 | 15 | 2026-11-26 – 2026-11-26 | 5 | 0 | 0 | [1](https://github.com/pypa/packaging/actions/runs/45911786628) |
| `pytest-dev/pytest` | 818 | 15 | 2026-11-26 – 2026-11-26 | 1 | 2 | 3 | [32](https://github.com/pytest-dev/pytest/actions/runs/45890405054) |
| `python/cpython` | 2500 | 15 | 2026-11-26 – 2026-11-26 | 3 | 0 | 0 | [2](https://github.com/python/cpython/actions/runs/45910888694) |
| `tox-dev/tox` | 2500 | 15 | 2026-11-26 – 2026-11-26 | 3 | 0 | 0 | [0](https://github.com/tox-dev/tox/actions/runs/45820960669) |
| `pypa/pip` | 590 | 15 | 2026-11-25 – 2026-11-26 | 2 | 0 | 0 | [38](https://github.com/pypa/pip/actions/runs/45913928914) |

### Expanded screening

The direct PR count in this table requires one matching PR reference for the run's base repository. It is a screening signal from the first page.

| Repository | Reason for inclusion | Reported API total | Sampled runs | Sample creation span (UTC) | Workflow paths | Sampled reruns | Direct PR links | Reported jobs in probed first attempt |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `dbt-labs/dbt` | Transformation tooling | 2500 | 15 | 2026-11-26 – 2026-11-26 | 6 | 0 | 6 | [1](https://github.com/dbt-labs/dbt/actions/runs/45914100890) |
| `duckdb/duckdb` | Analytical database | 2500 | 15 | 2026-11-26 – 2026-11-26 | 1 | 1 | 0 | [0](https://github.com/duckdb/duckdb/actions/runs/45890354426) |
| `apache/airflow` | Orchestration and matrix CI | 2500 | 15 | 2026-11-26 – 2026-11-26 | 2 | 3 | 0 | [0](https://github.com/apache/airflow/actions/runs/45910197366) |
| `pandas-dev/pandas` | Data library with platform matrices | 2500 | 15 | 2026-11-26 – 2026-11-26 | 6 | 0 | 0 | [2](https://github.com/pandas-dev/pandas/actions/runs/45912897337) |
| `pola-rs/polars` | Mixed Python and Rust checks | 2500 | 15 | 2026-11-26 – 2026-11-26 | 9 | 0 | 0 | [1](https://github.com/pola-rs/polars/actions/runs/45902743346) |
| `ibis-project/ibis` | Backend compatibility checks | 2500 | 15 | 2026-11-26 – 2026-11-26 | 7 | 0 | 0 | [0](https://github.com/ibis-project/ibis/actions/runs/45853472477) |
| `dlt-hub/dlt` | Ingestion and integration tests | 415 | 15 | 2026-11-24 – 2026-11-26 | 1 | 2 | 7 | [93](https://github.com/dlt-hub/dlt/actions/runs/45702309865) |
| `apache/superset` | BI application with integration tests | 2500 | 15 | 2026-11-26 – 2026-11-26 | 15 | 0 | 0 | [10](https://github.com/apache/superset/actions/runs/45909906541) |
| `astral-sh/ruff` | Mixed Rust and Python lint and test workflows | 2500 | 15 | 2026-11-26 – 2026-11-26 | 5 | 1 | 5 | [50](https://github.com/astral-sh/ruff/actions/runs/45896517219) |
| `fastapi/fastapi` | Service framework and compatibility CI | 2475 | 15 | 2026-11-24 – 2026-11-26 | 6 | 0 | 9 | [1](https://github.com/fastapi/fastapi/actions/runs/45784310332) |
| `encode/httpx` | Focused HTTP library test surface | 63 | 15 | 2026-11-24 – 2026-11-26 | 1 | 0 | 0 | [5](https://github.com/encode/httpx/actions/runs/45889602602) |
| `pypa/hatch` | Packaging workflows and Python compatibility | 564 | 15 | 2026-11-25 – 2026-11-26 | 5 | 0 | 0 | [20](https://github.com/pypa/hatch/actions/runs/45767742619) |

## Recognisable open-source case studies

After the 20-repository screening, check additional public projects that a general recruiting audience may recognise. Use the same completed PR-run filters over November 1–26, 2026 UTC. Read 50 rows per repository page and isolate the target workflow by path. These newer checks emphasise named test workflows and the feasibility of a controlled experiment.

| Public project | Target workflow | Repository rows read | Distinct workflow runs | Observed creation dates (UTC) | Direct PR links | Reruns |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| `microsoft/TypeScript` | `ci.yml` | 400 | 200 | 2026-11-20 to 2026-11-26 | 64 | 18 |
| `google/guava` | `ci.yml` | 250 | 126 | 2026-11-09 to 2026-11-26 | 16 | 1 |
| `docker/compose` | `ci.yml` | 1,432 | 293 | 2026-11-01 to 2026-11-26 | 3 | 38 |
| `google/googletest` | `ci.yml` | 128 | 59 | 2026-11-06 to 2026-11-26 | 6 | 0 |
| `vercel/next.js` | `build_and_test.yml` | 250 | 104 | 2026-11-26 | 30 | 2 |

TypeScript is the lead candidate for the portfolio case. All 200 selected runs share workflow ID 73. We read the first attempt of every rerun. Two runs changed from `failure` to `success`. The [pinned example](https://github.com/microsoft/TypeScript/actions/runs/45299141445) has 29 distinct jobs on each of two attempts. Its [workflow definition](https://github.com/microsoft/TypeScript/blob/399a95c9715b0cdf77aa8a23cf9cf557d8585b41/.github/workflows/ci.yml) uses a matrix and local actions. Reproduction on a fork or a controlled test has yet to be verified.

Guava is a secondary comparison. Its [example](https://github.com/google/guava/actions/runs/45266696694) moved from failure to success, and both attempts report 11 jobs. The workflow includes secret references, so assess the portability of a specific job before proposing a full replay. The [Next.js example](https://github.com/vercel/next.js/actions/runs/45889453579) reported 109 jobs in each probed attempt, and the recent cohort covers one day. Keep it in reserve pending a wider date sample.

VS Code and GitHub Docs returned mixed workflow paths in their first 30 rows. React's canonical repository `react/react` returned six workflow paths in its first 50 rows. The ONNX Runtime runs query returned HTTP 404 through the available API route. These candidates remain screening observations.

### Container tooling case

Check Docker Compose, AWS CDK, AWS SDK for JavaScript, Netflix DGS, Next.js, and React for a third portfolio case. Docker Compose supplies a container tooling workload alongside the TypeScript compiler and Java library. The initial depth checks found 40 PR build runs in 300 AWS CDK rows, 50 PR build runs in 200 AWS SDK rows, and 43 CI runs in the 86 Netflix DGS rows for the window. Next.js remains a one-day sample. The React screening page spans six workflow paths.

For Docker Compose, split the date filter into November 1–15 and November 16–26 UTC. The 29 pages returned all 840 and 592 repository rows reported by the API, respectively, with distinct run IDs across both windows. Workflow ID 12764968 accounts for 175 and 118 runs. Five selected successful reruns were checked against their first attempts. Three went from `failure` to `success`; the other two began with `action_required`. This evidence confirms cases and does not estimate a failure recovery rate. The [pinned example](https://github.com/docker/compose/actions/runs/45774420263) has 57 distinct jobs in each attempt at the [same workflow revision](https://github.com/docker/compose/blob/f013c10e3eec04e0e8c39d9a36587e9b58acf0ed/.github/workflows/ci.yml).

## Decision

- Lead with `microsoft/TypeScript` in the portfolio analysis. Use the test workflow as an observational baseline and select a specific optimisation experiment only after establishing a reproducible baseline with equivalent tests.
- Use `google/guava` and `docker/compose` as the two portfolio comparisons. Compare outcomes and rerun counts within each workflow. Identify the observation window and sample size for each case.
- Keep `pytest-dev/pytest` as the reference for the current offline fixtures. The deeper November query found 250 distinct runs of the same test workflow, and an upstream failure-to-success case has complete job pages for both attempts.
- Keep `dlt-hub/dlt` as the strongest data-stack comparator. In the November 1–26 UTC depth check, five 50-row pages returned 155 distinct runs for `.github/workflows/main.yml`. Of those, 40 had reruns and 64 had direct PR links (41.3%). The [example failure-to-success run](https://github.com/dlt-hub/dlt/actions/runs/45702309865) returned 93 jobs in its first attempt. Its pinned workflow references secrets, so validating reproducibility requires checking which jobs can run with public inputs. The depth check uses the same completed PR-run filters as the initial validation.
- Use `pypa/packaging` and `pypa/pip` as diagnostic comparisons. Review `duckdb/duckdb`, `apache/airflow`, `astral-sh/ruff`, and `fastapi/fastapi` if a second full comparator is needed. They would require bounded per-workflow queries and additional job probes before inclusion.
- Defer the remaining candidates for the first release. Some have low observed volume. Others need narrower retrieval windows or workflow isolation to distinguish test jobs from checks such as labeling, publishing, or documentation.

The expanded pool supports run- and attempt-level work. TypeScript has 32% direct PR coverage in the sampled workflow. Keep PR-level metrics out of the first release until a linkage method is validated.

## Validation sequence

1. Inspect recent 50-run pages per shortlisted repository over a fixed November window. Extend the depth only for promising workflows. Use smaller date windows when complete enumeration would exceed the API limit. Record workflow-level sample size, direct attachment coverage, and reruns.
2. Try exact commit-to-PR lookup on a small sample of runs with missing direct metadata. Keep unresolved and ambiguous records visible.
3. Inspect both attempts and every retrievable job for one confirmed failure-to-success run. Identify a pinned upstream reference and a controlled reproduction path.
4. Retain public technical identifiers and timing fields in a minimal sample. Add deterministic cases with known KPI values.
