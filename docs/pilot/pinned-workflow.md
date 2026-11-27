# Pinned workflow and replay

## TypeScript case

| Item | Value |
| --- | --- |
| Repository | `microsoft/TypeScript` |
| Workflow | [`.github/workflows/ci.yml` at the run head](https://github.com/microsoft/TypeScript/blob/399a95c9715b0cdf77aa8a23cf9cf557d8585b41/.github/workflows/ci.yml) |
| Run head SHA | `399a95c9715b0cdf77aa8a23cf9cf557d8585b41` |
| Public evidence | [Run 45299141445](https://github.com/microsoft/TypeScript/actions/runs/45299141445) |
| Attempt 1 | `failure`, started at `2026-11-24T00:40:59Z` |
| Attempt 2 | `success`, started at `2026-11-24T16:07:29Z` |

The attempt jobs API returned 29 entries per attempt. In attempt 2, 27 entries have start times before that attempt's start. `codegen` and `required` are the two jobs that started during the second attempt. For example, `smoke` appears under both attempts with different job IDs and identical start and end times. Keep the API's attempt job inventory, and use job and attempt timestamps when counting work that started during a rerun. Treat missing timestamps as unknown.

The public `smoke` job ran in the GitHub Actions runner group. Its lifetime was 286 seconds from `2026-11-24T00:41:04Z` to `2026-11-24T00:45:50Z`. The build step took 228 seconds, while the two compiler checks took 17 and 2 seconds. These timings describe one observed execution. The race-enabled build is the first optimisation candidate to investigate once a controlled baseline passes.

### Controlled TypeScript smoke baseline

Run the pinned `smoke` sequence in [TypeScript smoke baseline](../../.github/workflows/typescript-smoke-baseline.yml). It uses Ubuntu 24.04, Node.js 24.22.1, npm 11.21.1, Go 1.27.2, and the upstream lockfile. It records the exact revision, host or runner image, tool versions, and individual wall times. Cache restoration is disabled for the reference run. The rest of upstream CI includes a wider test matrix, PR context, a Microsoft runner, and coverage integration. The controlled result will apply to the `smoke` job only.

For a local Linux run, prepare the same tool versions, Python 3, and a working C compiler for the race-enabled Go build. Obtain a clean checkout of the revision above and run this from the portfolio repository:

```console
python3 scripts/run-typescript-smoke.py /path/to/pinned-typescript-checkout
```

This session reached the workflow definition and public job metadata through the GitHub API. Direct Git access to the source checkout and DNS resolution for the archive host failed, so the compiler build and the two compiler checks have yet to run under the controlled settings. After owner approval and publication to the default branch, dispatch the workflow and record the run link, runner image version, step outcomes, and durations here. Establish a passing baseline with both compiler checks before testing an optimisation. Keep race detection and both compiler checks in the baseline and treatment.

## pytest fixture provenance

| Item | Value |
| --- | --- |
| Repository | `pytest-dev/pytest` |
| Workflow | [`.github/workflows/test.yml` at the run head](https://github.com/pytest-dev/pytest/blob/d6e7262ea3ea0b44f99b3b92258a1d8efc9bcc2a/.github/workflows/test.yml) |
| Run head SHA | `d6e7262ea3ea0b44f99b3b92258a1d8efc9bcc2a` |
| Evidence | [Run 45890405054](https://github.com/pytest-dev/pytest/actions/runs/45890405054) |
| Attempt 1 | `failure`, started at `2026-11-26T20:21:07Z`, 32 jobs |
| Attempt 2 | `success`, started at `2026-11-26T20:35:32Z`, 32 jobs |

Both attempt endpoints reported the same run head SHA. The pinned workflow file has a package-build job, a test matrix, and external actions and dependencies. The run was triggered by a pull request. A manual dispatch at the run head cannot guarantee the same PR checkout context, runner image, or cache state. Historical attempt metadata establishes the failure-to-success sequence. A new upstream execution remains unverified.

## Offline data replay

The pilot replay checks the run, attempt, and job data path and reproduces the recovery result offline. It is a separate case from running the pytest suite on GitHub-hosted runners. It supports data and KPI verification. It carries no estimate of the original workflow's runtime or the reason for the first failure.

The replay depends on the fixture files and tests prepared in issue #4. Integrate those files before this workflow. Use the following command in both environments:

```console
python -m unittest discover -s tests -p test_pilot_fixtures.py -v
```

The GitHub Actions workflow uses an Ubuntu runner and Python 3.12. The fixture tests also run locally without GitHub credentials. After approval and publication, dispatch `Pilot replay` at the reviewed reference. Record the resolved SHA, runner image version, and resulting run link in issue #3. Repeat against the same SHA if verification requires a rerun. Use the pinned upstream case only as documented source evidence.
