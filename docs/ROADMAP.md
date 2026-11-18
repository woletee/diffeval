# diffeval PR roadmap

Implementation is a sequence of small pull requests into `main`. Each PR is reviewable on its own. Each new or edited `.py` file stays at or under 20 code lines, using the rule in `docs/DESIGN.md`. Open decisions D1–D14 in that document are settled before the PR that depends on them. Until then, the sequence below follows the recommended option.

Do not start the next PR until the previous one has merged. That keeps each diff to the modules listed here. This pull request is docs only. It does not add the package.

A PR is ready to merge when:

- pytest passes on Python 3.10, 3.11, and 3.12
- every `.py` file it adds or edits has at most 20 code lines
- new behavior has a CPU test that does not download weights
- a missing optional library skips that metric and still writes the report, once the runner exists

v1 is done at PR16: the package installs, `diffeval run --backend dummy --suite core` writes `results.json` and `report.html`, tests pass in CI, and the README covers install, the quickstart, extending a task, metric, or backend, and the rule that metric numbers are checked against the published reference.

## PR1 — Skeleton and registry

Goal: an installable package whose only behavior is the registry, with CI running the registry tests.

Modules:

- `pyproject.toml` — name `diffeval`, Python `>=3.10`, Apache-2.0, setuptools src layout, `dev` extra with pytest, no runtime dependencies yet
- `LICENSE` — Apache-2.0
- `.github/workflows/ci.yml` — pytest on 3.10, 3.11, and 3.12
- `src/diffeval/__init__.py` — `__version__`
- `src/diffeval/registry/tables.py`
- `src/diffeval/registry/register.py`
- `src/diffeval/registry/lookup.py`
- `src/diffeval/registry/names.py`
- `src/diffeval/registry/unregister.py`
- `tests/registry/test_register.py`
- `tests/registry/test_duplicate.py`
- `tests/registry/test_missing.py`
- `tests/registry/test_unregister.py`

Tested: register then get returns the same object; a second different object on that name raises; an unknown name raises `KeyError` and the message lists known names; unregister removes the name.

Works at the end: `pip install -e ".[dev]"` and `pytest`. There is no CLI yet. `import diffeval` exposes the version.

## PR2 — Records and YAML suites

Goal: load a prompt and seed suite from YAML. Depends on D4 (recommended: YAML).

Modules:

- `pyproject.toml` — add `pyyaml`
- `src/diffeval/types/request.py`
- `src/diffeval/types/sample.py`
- `src/diffeval/types/prompt.py`
- `src/diffeval/types/suite.py`
- `src/diffeval/types/context.py`
- `src/diffeval/types/result.py`
- `src/diffeval/types/result_rules.py`
- `src/diffeval/tasks/errors.py`
- `src/diffeval/tasks/read_yaml.py`
- `src/diffeval/tasks/fields_text.py`
- `src/diffeval/tasks/fields_size.py`
- `src/diffeval/tasks/fields_seeds.py`
- `src/diffeval/tasks/prompt_id.py`
- `src/diffeval/tasks/one_prompt.py`
- `src/diffeval/tasks/fields_prompts.py`
- `src/diffeval/tasks/fields_metrics.py`
- `src/diffeval/tasks/fields_paths.py`
- `src/diffeval/tasks/build_suite.py`
- `src/diffeval/tasks/from_mapping.py`
- `src/diffeval/tasks/load_path.py`
- `src/diffeval/tasks/resolve.py` — filesystem path only in this PR; registry lookup is wired when `core` is registered in PR10
- `tests/tasks/test_duplicate_id.py`
- `tests/tasks/test_relative_reference.py`

Tested: a YAML file with two prompts that share an id raises `SuiteError`. A relative `reference_dir` resolves next to the file. Width, height, and seeds survive the load.

Works at the end: `load_path` returns a `Suite`. Nothing generates images yet.

## PR3 — Dummy backend

Goal: deterministic RGB images from a prompt and a seed.

Modules:

- `pyproject.toml` — add `pillow`
- `src/diffeval/backends/protocol.py`
- `src/diffeval/backends/noop_prepare.py`
- `src/diffeval/backends/__init__.py` — import the dummy backend so it registers
- `src/diffeval/backends/dummy/colors.py`
- `src/diffeval/backends/dummy/box.py`
- `src/diffeval/backends/dummy/draw.py`
- `src/diffeval/backends/dummy/render.py`
- `src/diffeval/backends/dummy/generate.py`
- `src/diffeval/backends/dummy/describe.py`
- `src/diffeval/backends/dummy/from_config.py`
- `src/diffeval/backends/dummy/backend.py`
- `src/diffeval/plugins.py` — import backends
- `src/diffeval/__init__.py` — call the plugin load
- `tests/dummy/test_same_seed.py`
- `tests/dummy/test_other_seed.py`

Tested: the same prompt and seed produce the same bytes. A different seed produces different bytes. `describe()` reports `device=cpu` and `attention_backend=none`.

Works at the end: `BACKENDS["dummy"].from_config({...}).generate([...])` returns PIL images. Batch size does not change the bytes of a given prompt and seed.

## PR4 — Metric results and aggregate

Goal: mean and sample std across seeds, with skipped seeds left out of the mean. Depends on D9 (recommended: sample std, null when `n < 2`).

Modules:

- `src/diffeval/metrics/protocol.py`
- `src/diffeval/metrics/ok.py`
- `src/diffeval/metrics/skipped.py`
- `src/diffeval/aggregate/names.py`
- `src/diffeval/aggregate/series.py`
- `src/diffeval/aggregate/mean.py`
- `src/diffeval/aggregate/sample_std.py`
- `src/diffeval/aggregate/row.py`
- `src/diffeval/aggregate/table.py`
- `tests/aggregate/test_mean_std.py`
- `tests/aggregate/test_one_seed.py`
- `tests/aggregate/test_skipped.py`

Tested: values 2 and 4 give mean 3 and std `sqrt(2)`. One value gives that mean and a null std. Two skipped seeds give a null mean, status `skipped`, and `n` 0.

Works at the end: aggregation is pure and has no generator behind it.

## PR5 — Runner, PNGs, and JSON

Goal: generate every seed, save PNGs, call metrics, and write `results.json`. Real metrics are not registered yet; tests register a tiny metric through the registry and unregister it afterward.

Modules:

- `src/diffeval/runner/options.py`
- `src/diffeval/runner/requests.py`
- `src/diffeval/runner/save_png.py`
- `src/diffeval/runner/relpath.py`
- `src/diffeval/runner/metric_device.py`
- `src/diffeval/runner/safe_metric.py`
- `src/diffeval/runner/one_seed.py`
- `src/diffeval/runner/seeds.py`
- `src/diffeval/runner/payload.py`
- `src/diffeval/runner/write_json.py`
- `src/diffeval/runner/run.py`
- `tests/runner/test_seed_mean.py`

Tested: a two-prompt suite and a metric that returns the seed produce per-seed values 2 and 4, mean 3, sample std `sqrt(2)`, and one PNG per prompt per seed. Paths in JSON are relative. A metric that raises becomes status `error` and the PNGs are still written.

Works at the end: `run_evaluation` writes `results.json` and `images/seed_<n>/<prompt_id>.png`. Reports are not written yet.

## PR6 — Versions, GPU, and attention flags

Goal: the JSON records package versions, the GPU, and PyTorch attention flags, plus the backend `attention_backend` from `describe()`.

Modules:

- `src/diffeval/system/version_of.py`
- `src/diffeval/system/versions.py`
- `src/diffeval/system/gpu_cuda.py`
- `src/diffeval/system/gpu_mps.py`
- `src/diffeval/system/gpu.py`
- `src/diffeval/system/sdp_flags.py`
- `src/diffeval/system/describe.py`
- extend `runner/payload.py` only if it stays within 20 code lines; otherwise add `runner/payload_system.py` and call it from `runner/run.py`

Tested: on the CI runner, `versions.diffeval` is set, `versions.torch` is null, `system.gpu` is null, and `backend.attention_backend` is `none` for the dummy backend. The keys `torch`, `diffusers`, `transformers`, and the FID/KID library name exist even when the version is null.

Works at the end: a dummy run's JSON is enough to see what was installed and that no GPU was used.

## PR7 — CLI

Goal: `diffeval run` and `diffeval list`. Depends on D5 (recommended: argparse).

Modules:

- `pyproject.toml` — script `diffeval = diffeval.cli.main:main`
- `src/diffeval/__main__.py`
- `src/diffeval/cli/csv_ints.py`
- `src/diffeval/cli/csv_names.py`
- `src/diffeval/cli/run_parser_model.py`
- `src/diffeval/cli/run_parser_eval.py`
- `src/diffeval/cli/parser.py`
- `src/diffeval/cli/output_dir.py`
- `src/diffeval/cli/config.py`
- `src/diffeval/cli/print_registered.py`
- `src/diffeval/cli/command_list.py`
- `src/diffeval/cli/command_run.py`
- `src/diffeval/cli/main.py`
- `tests/cli/test_list.py`
- `tests/cli/test_unknown_suite.py`
- `tests/cli/test_console_script.py`

Tested: `main(["list", "backends"])` prints `dummy`. An unknown suite exits 2. The console script runs a YAML suite through the dummy backend and leaves `results.json` on disk. `--seeds` overrides the file.

Works at the end: a user can point `--suite` at a YAML file and `--backend dummy` and get images plus JSON. The stdout table is not formatted yet; the command prints the output paths. Strict mode lands with the table in PR8, where skipped metrics are visible.

## PR8 — Console table and Markdown report

Goal: print the aggregate table and write `report.md`.

Modules:

- `src/diffeval/report/number.py`
- `src/diffeval/report/direction.py`
- `src/diffeval/report/markdown_row.py`
- `src/diffeval/report/markdown.py`
- `src/diffeval/report/console_widths.py`
- `src/diffeval/report/console.py`
- `src/diffeval/runner/write_reports.py` — markdown only until PR9
- `src/diffeval/cli/command_run.py` — print `console.py` output; split the print into `cli/print_paths.py` if `command_run.py` would pass 20 code lines

Tested: the markdown contains a row per metric with mean, std, and direction. A null mean renders as `n/a`.

Works at the end: the command prints the table and writes `report.md` next to `results.json`.

## PR9 — HTML report

Goal: a static HTML report with an image grid. Depends on D7 (recommended: a template file, no template engine).

Modules:

- `src/diffeval/report/html_row.py`
- `src/diffeval/report/html_figure.py`
- `src/diffeval/report/html_grid.py`
- `src/diffeval/report/html_page.py`
- `src/diffeval/report/templates/page.html`
- `tests/runner/test_html_escape.py`

Tested: a prompt that contains `<script>` is stored in the HTML as escaped text. The report contains one `<img>` per sample, and the `src` is the relative PNG path. The page includes the sentence that metric numbers have to be checked against the published reference before they are compared to a paper.

Works at the end: `report.html` opens without a network connection and shows the grid beside the table.

## PR10 — Bundled `core` suite

Goal: `diffeval run --backend dummy --suite core` writes JSON and HTML. Depends on D13 (recommended: ship four synthetic reference PNGs).

Modules:

- `src/diffeval/tasks/load_bundled.py`
- `src/diffeval/tasks/core.py`
- `src/diffeval/tasks/__init__.py`
- `src/diffeval/tasks/resolve.py` — registry name as well as YAML path
- `src/diffeval/tasks/suites/core.yaml`
- `src/diffeval/tasks/suites/references/core/*.png` — four drawings, one per prompt id
- `tests/tasks/test_core_suite.py`
- `tests/runner/test_dummy_json_html.py`
- `.github/workflows/ci.yml` — run the smoke command after pytest

`core.yaml` sets name `core`, seeds `[0, 1]`, 512×512, metrics `clip_score`, `cmmd`, `fid`, `kid`, and `reference_dir: references/core`. Prompts are a red cube, a blue sphere, a green triangle, and a yellow star, with those ids.

Tested: the bundled suite lists those four ids and both seeds, and the reference directory contains four PNGs. The smoke command writes `results.json` and `report.html` with eight images. Metric rows are absent or skipped until PR11–PR13 register them; the test allows either until those PRs land, then asserts the four names.

Works at the end: the acceptance command runs on CPU with no downloads. `diffeval list tasks` shows `core`.

## PR11 — CLIP score

Goal: reference-free CLIP score, skipped when the metrics extra is missing. Depends on D2 (recommended: Hessel et al. 2021, ViT-B/32, weight 2.5).

Modules:

- `pyproject.toml` — `metrics` extra with torch and transformers
- `src/diffeval/metrics/__init__.py`
- `src/diffeval/metrics/clip/protocol.py`
- `src/diffeval/metrics/clip/formula.py`
- `src/diffeval/metrics/clip/load.py`
- `src/diffeval/metrics/clip/features.py`
- `src/diffeval/metrics/clip/score.py`
- `src/diffeval/metrics/clip/metric.py`
- `tests/clip/test_formula.py`

Tested: cosines `1, 0, -1` produce mean `2.5 / 3`. With the metrics extra absent, a dummy `core` run records `clip_score` as `skipped` and still writes the report. The protocol in JSON names the model, the crop, the weight, and the paper.

Works at the end: installing the metrics extra and running a suite scores CLIP against the prompts for each seed. CI does not install that extra and does not download weights.

## PR12 — CMMD

Goal: CMMD against `reference_dir` or a precomputed `.npy`. Depends on D3 (recommended: official estimator, no extra L2 normalization).

Modules:

- `pyproject.toml` — add `numpy` to the core dependencies
- `src/diffeval/metrics/images.py`
- `src/diffeval/metrics/count_warning.py`
- `src/diffeval/metrics/cmmd/protocol.py`
- `src/diffeval/metrics/cmmd/mmd.py`
- `src/diffeval/metrics/cmmd/resize.py`
- `src/diffeval/metrics/cmmd/embed_batch.py`
- `src/diffeval/metrics/cmmd/embed_paths.py`
- `src/diffeval/metrics/cmmd/score.py`
- `src/diffeval/metrics/cmmd/metric.py`
- `tests/cmmd/test_zero.py`
- `tests/cmmd/test_known_pair.py`

Tested: identical embeddings score 0. The one-dimensional pair `0` and `10` scores `1000 * (2 - 2 * exp(-0.5))`, which is the official diagonal-included RBF with sigma 10. A suite with no reference and no `.npy` skips. The protocol says embeddings are not L2-normalized and names the 336 bicubic resize.

Works at the end: with the metrics extra installed, CMMD runs per seed on the reference folder. `core` warns that four images are not the paper's COCO setup.

## PR13 — FID and KID

Goal: FID and KID by calling a published library, not an in-repo Inception. Depends on D1 (recommended: clean-fid, `mode="clean"`).

Modules:

- `pyproject.toml` — add the chosen library to the `metrics` extra
- `src/diffeval/metrics/distribution/protocol.py`
- `src/diffeval/metrics/distribution/kwargs_folder.py`
- `src/diffeval/metrics/distribution/kwargs_stats.py`
- `src/diffeval/metrics/distribution/seed_numpy.py`
- `src/diffeval/metrics/distribution/call.py`
- `src/diffeval/metrics/fid/guard.py`
- `src/diffeval/metrics/fid/metric.py`
- `src/diffeval/metrics/kid/guard.py`
- `src/diffeval/metrics/kid/metric.py`
- `tests/distribution/test_folder_kwargs.py`
- `tests/distribution/test_stats_kwargs.py`
- `tests/distribution/test_seeded_call.py`

If D1 is torch-fidelity instead, the same module paths remain and the keyword tests assert that library's arguments and its documented resize.

Tested: folder mode passes `mode="clean"`, reference as `fdir1`, generated as `fdir2`, `num_workers=0`, and `model_name="inception_v3"` for FID only. Stats mode passes `dataset_name`, `dataset_res`, and `dataset_split` and does not pass a second folder. Two calls with the same seed see the same NumPy draw, and the previous NumPy state is restored. Fewer than two images skips. The JSON protocol states the resize and that diffeval does not pre-resize.

Works at the end: with the metrics extra installed, FID and KID run per seed (D8) and the aggregate carries mean and std. CI still uses the fake-module tests only.

## PR14 — GenEval stub and optional extras

Goal: suites can name `geneval`, and the heavy stacks stay off the default install. Depends on D11 (recommended: skipped stub, no fake VBench score).

Modules:

- `pyproject.toml` — extras `geneval` and `video` without the detector or VBench pins
- `src/diffeval/metrics/geneval/tags.py`
- `src/diffeval/metrics/geneval/protocol.py`
- `src/diffeval/metrics/geneval/metric.py`
- `tests/geneval/test_skipped.py`
- `tests/cli/test_strict.py`

Tested: `compute` returns `skipped`, a null value, and a `by_tag` dict with the six GenEval keys. `diffeval list metrics` includes `geneval`. `--metrics geneval --strict` writes the report and exits 2.

Works at the end: a suite that lists `geneval` finishes. The detector is not imported.

## PR15 — Diffusers text-to-image backend

Goal: `diffeval run --pipeline <id> --suite core` loads `AutoPipelineForText2Image`. Depends on D10 (recommended: schnell preset of 4 steps and guidance 0). No weight download in tests.

Modules:

- `pyproject.toml` — `diffusers` extra (torch, diffusers, transformers, accelerate, safetensors)
- `src/diffeval/backends/diffusers/presets.py`
- `src/diffeval/backends/diffusers/sampling.py`
- `src/diffeval/backends/diffusers/dtype_name.py`
- `src/diffeval/backends/diffusers/pick_device.py`
- `src/diffeval/backends/diffusers/coerce_dtype.py`
- `src/diffeval/backends/diffusers/missing_dep.py`
- `src/diffeval/backends/diffusers/load_kwargs.py`
- `src/diffeval/backends/diffusers/load_pipe.py`
- `src/diffeval/backends/diffusers/kwargs_prompt.py`
- `src/diffeval/backends/diffusers/kwargs_sampling.py`
- `src/diffeval/backends/diffusers/kwargs_size.py`
- `src/diffeval/backends/diffusers/kwargs_generator.py`
- `src/diffeval/backends/diffusers/call_kwargs.py`
- `src/diffeval/backends/diffusers/attention_name.py`
- `src/diffeval/backends/diffusers/attention_sdpa.py`
- `src/diffeval/backends/diffusers/attention_eager.py`
- `src/diffeval/backends/diffusers/attention_xformers.py`
- `src/diffeval/backends/diffusers/attention_apply.py`
- `src/diffeval/backends/diffusers/one_batch.py`
- `src/diffeval/backends/diffusers/generate.py`
- `src/diffeval/backends/diffusers/describe.py`
- `src/diffeval/backends/diffusers/from_config.py`
- `src/diffeval/backends/diffusers/backend.py`
- `src/diffeval/backends/__init__.py` — also import this package
- `tests/diffusers/test_preset.py`
- `tests/diffusers/test_call_kwargs.py`
- `tests/diffusers/test_attention_name.py`
- `tests/diffusers/test_missing_dependency.py`

Tested: schnell with no flags resolves to 4 steps and guidance 0, both sourced from `preset`. A CLI step overrides only the step. An unknown model id leaves both values unset so the pipeline default applies. Call kwargs include a distinct CPU generator per request, omit steps when the value is unset, and forward width when the signature has `**kwargs`. Attention classification maps an `AttnProcessor2_0` instance to `sdpa` and an xformers processor to `xformers`. `prepare` without the extra raises an error that names `diffeval[diffusers]`.

Works at the end: `diffeval list backends` shows `diffusers` and `dummy`. A machine with the extra and a Hugging Face token can run the FLUX quickstart. CI does not.

## PR16 — README

Goal: the user-facing document for the package that PR1–PR15 built.

Modules:

- `README.md` — purpose, install (`pip install -e .`, plus the `diffusers`, `metrics`, and `dev` extras), quickstart for the dummy smoke command and for `diffeval run --pipeline black-forest-labs/FLUX.1-schnell --suite core`, `diffeval list`, the output files, how to add a YAML task, how to add a metric, how to add a backend, the metric protocols in short form, and a direct statement that metric numbers have to be validated against the published reference implementation and dataset before they are compared to a paper
- the line cap and the module tree stay in `docs/DESIGN.md`; the README links there instead of repeating the tree

Tested: no new runtime behavior. CI still runs pytest and the dummy `core` command.

Works at the end: a new reader can install the package, run the smoke command, and see where a new task, metric, or backend is registered.

## After v1

These are out of PR1–PR16. Each one should be its own later PR, still under the 20-line cap.

- fal and Replicate backends on the same `generate` / `describe` interface (D12)
- a real GenEval Mask2Former scorer behind the existing `geneval` name
- VBench and other video metrics, and a video backend
- full prompt suites for GenEval, T2I-CompBench, and COCO, as more YAML plus reference folders or clean-fid stats
- any change that would make a `core` smoke score look like a published table
