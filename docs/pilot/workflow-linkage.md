# Workflow selection and PR linkage

## Sampling

Query the [repository workflow runs API](https://docs.github.com/en/rest/actions/workflow-runs#list-workflow-runs-for-a-repository) with `event=pull_request`, `status=completed`, `created=2026-11-01..2026-11-26`, `per_page=50`, and `page=1..5`. The snapshot was collected on November 27, 2026. Read at most 250 rows per repository and verify uniqueness by run ID within each repository. Count workflow paths inside this repository-level sample. These are recent observations within the window, so workflow counts are sample coverage figures.

A directly linked run has exactly one PR reference whose base repository ID matches the run repository ID. The denominator is every completed run in the sample for that workflow, including cancelled or skipped runs. This measures availability of GitHub-provided linkage. A rerun is a distinct run with a latest `run_attempt` greater than one.

For each workflow, take the first ten distinct head SHAs with no direct PR reference in API order. Query [pull requests associated with each commit](https://docs.github.com/en/rest/commits/commits#list-pull-requests-associated-with-a-commit). Accept one result only when the base repository and PR head SHA both match. A full response page would remain unresolved until paginated. Keep this diagnostic separate from the direct coverage rate.

## Results

| Repository | Workflow | Repository API total | Repository rows read | Workflow rows | Direct PR links | Reruns | Cancelled or skipped | Exact SHA links in diagnostic sample |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `pytest-dev/pytest` | `.github/workflows/test.yml` | 314 | 250 | 250 | 28 (11.2%) | 7 | 63 | 0/10 |
| `pypa/packaging` | `.github/workflows/test.yml` | 1356 | 250 | 51 | 25 (49.0%) | 1 | 13 | 0/10 |
| `pypa/pip` | `.github/workflows/ci.yml` | 199 | 199 | 88 | 0 (0.0%) | 2 | 18 | 0/10 |

All 30 commit lookups returned empty lists. The fallback is inconclusive for the rest of the cohort. Historical commits can differ from a PR's current head SHA, so exact-head matching can also leave valid links unresolved.

The expanded source survey added `dlt-hub/dlt` as a fourth depth check with the same filters and page limits. Its API total and enumerated sample both equal 155. All runs use `.github/workflows/main.yml`. There are 64 direct PR links (41.3%), 40 reruns, and 25 cancelled or skipped runs. This follow-up used direct metadata. The 30 exact SHA lookups apply to the three workflows in the table.

## Decision

Use public `microsoft/TypeScript` CI as the lead case for run- and attempt-level analysis. With the same filters, the first eight repository pages yielded 400 distinct runs. Of these, 200 used `.github/workflows/ci.yml` (workflow ID 73), 64 had direct PR links (32%), and 18 had more than one attempt. Read the first attempt for all 18 reruns. Two were `failure → success`, eleven were `action_required → success`, four were `action_required → failure`, and one was `cancelled → success`. Count these as distinct categories. The exact-SHA fallback diagnostic was performed on the three original comparison workflows.

Keep `pytest-dev/pytest` and `.github/workflows/test.yml` as the reference for offline fixtures. Its sample has 250 runs and a confirmed [failure followed by a successful rerun](https://github.com/pytest-dev/pytest/actions/runs/45890405054). Keep `dlt-hub/dlt` as the data-stack comparator and retain packaging and pip for diagnostic comparisons.

Use public `google/guava` and `docker/compose` CI as portfolio comparisons. Guava's selected workflow has 126 sampled runs, 16 direct PR links (12.7%), and one rerun. For Docker Compose, enumerate the two November 1–15 and November 16–26 windows independently to stay below the API result cap, then check uniqueness across all 1,432 repository runs. Workflow ID 12764968 has 293 runs, three direct PR links (1.0%), and 38 reruns. Its [confirmed failure and recovery](https://github.com/docker/compose/actions/runs/45774420263) has complete job pages for both attempts. These Docker and Guava counts use direct PR metadata.

The planned PR-linked study requires three workflows with roughly 200 runs each and 80% reliable linkage. The depth checks have yet to identify a workflow that meets both targets. Leave PR-level claims out of v0.1 unless a new linkage method is validated independently. Preserve the run denominator explicitly.

For latency, show the median and the eligible count first. Before publishing P95, specify which terminal outcomes and timestamps qualify and evaluate the effective sample after filtering. The 250-run cohort merits that check for the all-workflow view. Smaller slices, including reruns, should show counts and medians until there are enough observations for a stable tail estimate. Avoid using `updated_at` as a proxy for a terminal timestamp.
