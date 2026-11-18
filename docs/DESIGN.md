# diffeval design

diffeval is an evaluation harness for image and video diffusion models. One command generates a fixed prompt and seed suite, scores it, and writes three artifacts: a results JSON file, a text table, and a static HTML report with image grids.

```bash
diffeval run --pipeline black-forest-labs/FLUX.1-schnell --suite core
```

Tasks are benchmarks (prompt and seed suites such as a bundled `core` suite, and later GenEval, T2I-CompBench, or FID/KID on COCO). Backends are model runtimes. The first backend is a Hugging Face Diffusers text-to-image pipeline. A dummy backend exists for CPU tests. API backends such as fal and Replicate are a later backend behind the same interface. Metrics are CLIP score, CMMD, FID, and KID, plus a GenEval stub. Heavy stacks (the GenEval detector, VBench, video) stay optional extras.

This document is the layout to review before implementation. It assumes the recommended side of each open decision in the last section. `docs/ROADMAP.md` splits the work into small pull requests.

## Line cap

Every `.py` file in the package and in `tests/` has at most 20 lines of code.

A line counts when it is a physical line of code. Blank lines, comment-only lines, and docstring lines do not count. Imports count. A signature or a call that wraps onto a second physical line counts as two lines. `pyproject.toml`, YAML suites, HTML templates, Markdown, the license, and GitHub Actions YAML do not count toward the cap. Decision D6 is whether to extend the cap to those files.

The cap is held by giving each module one job:

- A leaf module defines one function, one dataclass, or one constant.
- A class module only binds those functions onto a class and registers the class. It does not contain the behavior.
- A composer module only calls other modules. It takes one options object so the `def` line stays a single physical line.
- If a body would pass 20 code lines, add another module. Do not raise the cap in an implementation PR.

Illustrative shape of a leaf (this is the counting rule, not a file to copy in as a larger module):

```python
"""Register one object under one name."""

def register(table: dict, name: str):
    def decorator(obj):
        if name in table and table[name] is not obj:
            raise ValueError(f"{name} is already registered")
        table[name] = obj
        return obj
    return decorator
```

That function is 8 code lines. The docstring does not count.

`plugins` modules import concrete tasks, metrics, and backends so their register calls run. A plugins module that would need more than 20 import lines is split (`plugins_metrics_a.py`, `plugins_metrics_b.py`). Package `__init__.py` files do not re-export the whole tree.

## How a run fits together

```
diffeval run
    -> resolve the suite (YAML path, or TASKS[name].load())
    -> BACKENDS[name].from_config(config).prepare()
    -> for each seed:
         backend.generate(requests for that seed)
         write uint8 RGB PNGs
         for each metric name:
             METRICS[name]().compute(samples, context)
    -> mean and sample std across seeds
    -> attach versions, GPU, attention backend, metric protocols
    -> results.json, report.md, report.html
    -> print the table
```

Importing `diffeval` loads plugins. Each concrete task, metric, and backend registers itself into one of three dicts: `TASKS`, `METRICS`, `BACKENDS`. The CLI and the runner only look up names. They do not import a concrete backend or metric by hand.

`diffeval list tasks`, `diffeval list metrics`, and `diffeval list backends` print `names(table)` and each object's `description`.

`--backend` chooses the backend. When `--backend` is omitted and `--pipeline` is set, the backend name is `diffusers`. The dummy backend is what CPU tests and the smoke command use.

One metric failure does not discard the images. `compute` returns `skipped` when an optional library or a reference set is missing, and `error` when it raises. The runner also catches an unexpected exception and stores it as `error`. `--strict` still writes the report, then exits with status 2 when any aggregate status is not `ok`.

## Registry

| Function | Signature | Job |
| --- | --- | --- |
| `register` | `register(table: dict, name: str) -> Callable` | Decorator. A second different object on the same name raises `ValueError`. |
| `get` | `get(table: dict, name: str, kind: str) -> object` | Lookup. `KeyError` names the kind and the known keys. |
| `names` | `names(table: dict) -> list[str]` | Sorted keys, for `diffeval list`. |
| `unregister` | `unregister(table: dict, name: str) -> None` | Test cleanup. |

`tables.py` holds the three dicts and nothing else. Registration is by name, not by inheritance. A test that inserts a fake metric removes it before the test ends.

## Core interfaces

Records are dataclasses, one per module. Methods below are the contracts composers call. `Protocol` modules document them; classes do not have to subclass the protocol.

```python
def load(self) -> Suite: ...
```

`Task` also has `description: str`. `TASKS["core"].load()` reads the bundled YAML. A path ending in `.yaml` or `.yml` skips the registry and loads that file.

```python
@dataclass(frozen=True)
class Prompt:
    id: str
    prompt: str
    negative_prompt: str | None = None
    meta: dict | None = None

@dataclass(frozen=True)
class Suite:
    name: str
    description: str
    prompts: tuple[Prompt, ...]
    seeds: tuple[int, ...]
    width: int
    height: int
    metrics: tuple[str, ...]
    reference_dir: Path | None
    clean_fid_stats: dict | None
    cmmd_ref_embed: Path | None
    source: str
```

Prompt ids match `[A-Za-z0-9_-]+` so they are safe filenames. Seeds are a non-empty list of ints. `width` and `height` default to 512 when the file omits them. `metrics` defaults to `clip_score`, `cmmd`, `fid`, `kid`. A prompt may carry a `meta` mapping. The runner copies it onto the request and the sample unchanged, so a metric that needs per-prompt data, such as the questions a VQA judge asks, reads it from `sample.meta`.

```python
@dataclass(frozen=True)
class GenerationRequest:
    prompt_id: str
    prompt: str
    seed: int
    width: int
    height: int
    negative_prompt: str | None = None
    meta: dict | None = None

@dataclass
class Sample:
    prompt_id: str
    prompt: str
    seed: int
    width: int
    height: int
    image: object | None
    path: str | None
    negative_prompt: str | None = None
    meta: dict | None = None
```

```python
def from_config(self, config: dict) -> Backend: ...
def prepare(self) -> None: ...
def generate(self, requests: list[GenerationRequest]) -> list[Sample]: ...
def describe(self) -> dict: ...
```

`generate` returns one PIL RGB image per request, in order. Each image is seeded from that request's seed, so a sample does not depend on its position in the batch. `prepare` loads weights once. The dummy backend's `prepare` is a no-op.

`describe()` returns these keys: `name`, `pipeline`, `dtype`, `requested_dtype`, `steps`, `guidance`, `steps_source`, `guidance_source`, `batch_size`, `device`, `attention_backend`, `variant`. `steps_source` and `guidance_source` are `cli`, `preset`, or `pipeline-default`. The dummy backend sets `device` to `cpu` and `attention_backend` to `none`.

```python
@dataclass(frozen=True)
class EvalContext:
    generated_dir: Path
    reference_dir: Path | None
    device: str
    seed: int
    clean_fid_stats: dict | None
    cmmd_ref_embed: Path | None
    batch_size: int

@dataclass
class MetricResult:
    name: str
    value: float | None
    status: str
    error: str | None
    higher_is_better: bool | None
    details: dict
    protocol: dict

def compute(self, samples: list[Sample], context: EvalContext) -> MetricResult: ...
```

`status` is `ok`, `skipped`, or `error`. `ok` carries a finite float. `skipped` and `error` carry a null value and an `error` string. `protocol` is copied once into the results file so a reader can see the model, resize, and formula.

`Metric` also has `name`, `description`, `higher_is_better`, `requires_references`, and `protocol`.

```python
def aggregate(per_seed: list[dict]) -> dict: ...
```

For each metric, `mean` is the arithmetic mean of seeds whose status is `ok`. `std` is the sample standard deviation (`ddof=1`) when at least two seeds succeeded, and null otherwise. `per_seed` keeps nulls for seeds that did not score. `n` is the number of successful seeds. Aggregate `status` is `ok` when every seed succeeded, `partial` when some did, `skipped` when every seed skipped, and `error` when any seed errored and none succeeded.

```python
def run_evaluation(options: RunOptions) -> dict: ...
```

`RunOptions` holds the suite, backend name, backend config, output directory, optional seed override, optional metric override, and optional width and height. The function prepares the backend, scores every seed, builds the payload, writes the three artifacts, and returns the payload.

CLI entry:

```python
def main(argv: list[str] | None = None) -> int: ...
```

`0` means the report was written. `2` means the suite, backend, or metric name was unknown, generation failed, or `--strict` found a metric that is not `ok`.

## Results file

`results.json` uses `schema_version` 1.

- `created_at` is UTC.
- `suite` stores the name, description, source, width, height, prompts, reference directory, clean-fid stats, and CMMD embedding path.
- `backend` is `describe()`.
- `metric_device` is the device metrics used (`--device`, otherwise CUDA, otherwise MPS, otherwise CPU).
- `seeds` is the seeds actually used.
- `versions` includes `diffeval`, `python`, `numpy`, `pillow`, `pyyaml`, `torch`, `diffusers`, `transformers`, `accelerate`, and the FID/KID library. A package that is not installed is null.
- `system.platform` is the platform string. `system.gpu` is null on CPU, or the CUDA device name, index, count, and total memory. MPS is recorded as a GPU entry named `Apple MPS` when torch reports it.
- `system.torch_attention` is the PyTorch scaled-dot-product flags (`flash_sdp`, `mem_efficient_sdp`, `math_sdp`, `cudnn_sdp`) when torch is installed, and null otherwise. The processor the pipeline actually used is `backend.attention_backend`, not these flags.
- `metric_protocols` maps a metric name to its protocol dict.
- `per_seed[].samples[].path` is relative to the output directory, for example `images/seed_0/red_cube.png`.
- `aggregate` is the mean/std table.
- `outputs` names `results.json`, `report.md`, and `report.html`.

The console table and `report.md` show metric, status, mean, std, per-seed values, and direction (`higher` or `lower`). The HTML report repeats that table and an image grid grouped by prompt, with one figure per seed. Prompts are escaped. Image `src` values are the relative PNG paths. The page says that scores have to be checked against the published reference implementation and dataset, and that `core` is a smoke suite.

Images are uint8 RGB PNG at the requested resolution. FID/KID code does not resize them before calling the library. The library's own resizer is part of the protocol text.

## Module tree

Each row is one module and one job.

```
src/diffeval/
  __init__.py                         version string and plugin load
  __main__.py                         call cli.main
  plugins.py                          import tasks, metrics, and backends
  registry/tables.py                  TASKS, METRICS, BACKENDS dicts
  registry/register.py                register(table, name) decorator
  registry/lookup.py                  get(table, name, kind)
  registry/names.py                   sorted names
  registry/unregister.py              unregister for tests
  types/request.py                    GenerationRequest
  types/sample.py                     Sample
  types/prompt.py                     Prompt
  types/suite.py                      Suite
  types/context.py                    EvalContext
  types/result.py                     MetricResult
  types/result_rules.py               finite value and status rules
  tasks/errors.py                     SuiteError
  tasks/read_yaml.py                  read a YAML file to a mapping
  tasks/fields_text.py                name and description
  tasks/fields_size.py                width and height
  tasks/fields_seeds.py               seed list
  tasks/prompt_id.py                  id pattern
  tasks/one_prompt.py                 one prompt mapping
  tasks/fields_prompts.py             prompt list and duplicate ids
  tasks/fields_metrics.py             metric name list
  tasks/fields_paths.py               reference_dir, cmmd_ref_embed, clean_fid_stats
  tasks/build_suite.py                assemble a Suite
  tasks/from_mapping.py               composer from a mapping
  tasks/load_path.py                  filesystem YAML, resolve relative paths
  tasks/load_bundled.py               packaged core.yaml beside the module
  tasks/resolve.py                    path or TASKS lookup
  tasks/core.py                       register task "core"
  tasks/suites/core.yaml              four prompts, seeds 0 and 1, 512 square
  tasks/suites/references/core/       four synthetic reference PNGs
  backends/protocol.py                Backend protocol
  backends/noop_prepare.py            prepare that does nothing
  backends/dummy/colors.py            background and foreground from hashes
  backends/dummy/box.py               seed-shifted box
  backends/dummy/draw.py              rectangle, ellipse, or triangle
  backends/dummy/render.py            one PIL image
  backends/dummy/generate.py          generate requests in batch-size slices
  backends/dummy/describe.py          describe() for dummy
  backends/dummy/from_config.py       batch size and unused pipeline id
  backends/dummy/backend.py           bind and register "dummy"
  backends/diffusers/presets.py       published steps and guidance by model id
  backends/diffusers/sampling.py      cli, preset, or pipeline-default
  backends/diffusers/dtype_name.py    map dtype strings to torch dtypes
  backends/diffusers/pick_device.py   cuda, mps, or cpu
  backends/diffusers/coerce_dtype.py  float32 on CPU for float16 and bfloat16
  backends/diffusers/missing_dep.py   error telling the user to install the extra
  backends/diffusers/load_kwargs.py   from_pretrained keyword arguments
  backends/diffusers/load_pipe.py     AutoPipelineForText2Image and .to(device)
  backends/diffusers/kwargs_prompt.py prompt and negative_prompt
  backends/diffusers/kwargs_sampling.py steps and guidance when accepted
  backends/diffusers/kwargs_size.py   width and height when accepted
  backends/diffusers/kwargs_generator.py one CPU generator per seed
  backends/diffusers/call_kwargs.py   compose pipeline call kwargs
  backends/diffusers/attention_name.py classify the current processor
  backends/diffusers/attention_sdpa.py attach AttnProcessor2_0
  backends/diffusers/attention_eager.py attach AttnProcessor
  backends/diffusers/attention_xformers.py enable xformers
  backends/diffusers/attention_apply.py dispatch sdpa, xformers, eager, or detect
  backends/diffusers/one_batch.py     one pipeline call for a same-size batch
  backends/diffusers/generate.py      walk requests in batches
  backends/diffusers/describe.py      describe() after load
  backends/diffusers/from_config.py   require --pipeline
  backends/diffusers/backend.py       bind and register "diffusers"
  metrics/protocol.py                 Metric protocol
  metrics/ok.py                       build an ok MetricResult
  metrics/skipped.py                  build a skipped MetricResult
  metrics/images.py                   list PNG, JPEG, WEBP, BMP in a directory
  metrics/count_warning.py           warn when the sample count is below a paper's usual n
  metrics/clip/protocol.py           CLIPScore definition text
  metrics/clip/formula.py            w * max(cosine, 0) and the mean
  metrics/clip/load.py               CLIPModel and CLIPProcessor
  metrics/clip/features.py           L2-normalized image and text features
  metrics/clip/score.py              per-image scores for one seed, chunks of 32
  metrics/clip/sample_image.py       pixels, or the saved PNG when the runner dropped them
  metrics/clip/metric.py             register "clip_score"
  metrics/cmmd/protocol.py           CMMD definition text
  metrics/cmmd/mmd.py                minimum-variance RBF MMD, sigma 10, scale 1000, row blocks
  metrics/cmmd/resize.py             center crop, bicubic resize to 336
  metrics/cmmd/embed_batch.py        one CLIP vision batch, L2-normalized
  metrics/cmmd/embed_paths.py        embed image files in chunks of 32
  metrics/cmmd/score.py              reference folder or .npy against generated PNGs
  metrics/cmmd/metric.py             register "cmmd"
  metrics/distribution/protocol.py   shared FID/KID library, resize, and feature text
  metrics/distribution/kwargs_folder.py  reference dir and generated dir arguments
  metrics/distribution/kwargs_stats.py   precomputed dataset-stat arguments
  metrics/distribution/seed_numpy.py seed NumPy around the library call and restore it
  metrics/distribution/call.py       call the library for fid or kid
  metrics/fid/guard.py               require 2 images and a reference or stats
  metrics/fid/metric.py              register "fid"
  metrics/kid/guard.py               same guard for KID
  metrics/kid/metric.py              register "kid"
  metrics/geneval/tags.py            the six GenEval tag names
  metrics/geneval/protocol.py        stub protocol and tag schema
  metrics/geneval/metric.py          register "geneval" and return skipped
  aggregate/names.py                 metric names in first-seen order
  aggregate/series.py                per-seed values and statuses for one metric
  aggregate/mean.py                  arithmetic mean
  aggregate/sample_std.py            sample std, null below two values
  aggregate/row.py                   one aggregate row
  aggregate/table.py                 aggregate(per_seed)
  system/version_of.py               importlib.metadata version or null
  system/versions.py                 the versions dict
  system/gpu_cuda.py                 CUDA name, index, count, memory
  system/gpu_mps.py                  MPS entry
  system/gpu.py                      cuda, else mps, else null
  system/sdp_flags.py                torch SDPA kernel flags
  system/describe.py                 platform, gpu, torch_attention
  runner/options.py                  RunOptions
  runner/requests.py                 GenerationRequest list for one seed
  runner/save_png.py                 write one uint8 RGB PNG
  runner/relpath.py                  path relative to the output directory
  runner/metric_device.py            pick the metric device
  runner/safe_metric.py              call compute and catch exceptions
  runner/one_seed.py                 generate, save, score one seed
  runner/generate_save.py            generate in chunks of 64, save, drop pixels
  bench/fetch.py                     download a URL once
  bench/cmmd_samples.py              cmmd-pytorch sample PNGs
  bench/cmmd_check.py                diffeval-check-cmmd, expects 7.696
  bench/coco30k_files.py             COCO-30k captions and reference embeddings
  bench/coco30k_suite.py             suite mapping for the first N captions
  bench/coco30k_cli.py               diffeval-coco30k
  bench/coco30k_export.py            reference PNGs from the parquet shards
  bench/coco30k_images.py            diffeval-coco30k-images
  bench/published.py                 published COCO-30k CMMD by model id
  bench/table_row.py                 one Markdown row from results.json
  bench/table_cli.py                 diffeval-table
  runner/seeds.py                    loop seeds
  runner/payload.py                  assemble the JSON object
  runner/write_json.py               write results.json
  runner/write_reports.py            write report.md and report.html
  runner/run.py                      run_evaluation composer
  report/number.py                   format a float or n/a
  report/direction.py                higher or lower
  report/markdown_row.py             one markdown row
  report/markdown.py                 full markdown report
  report/console_widths.py           column widths
  report/console.py                  plain text table
  report/html_row.py                 one escaped table row
  report/html_figure.py              one escaped figure
  report/html_grid.py                grids grouped by prompt
  report/html_page.py                fill the template
  report/templates/page.html         static shell with placeholders
  cli/csv_ints.py                    parse --seeds
  cli/csv_names.py                   parse --metrics
  cli/run_parser_model.py            backend, pipeline, dtype, steps, guidance, device
  cli/run_parser_eval.py             suite, seeds, metrics, size, output, strict
  cli/parser.py                      argparse with run and list
  cli/output_dir.py                  default outputs/<utc>-<suite>-<backend>
  cli/config.py                      backend config dict from args
  cli/print_registered.py            print names and descriptions
  cli/command_list.py                list tasks, metrics, or backends
  cli/command_run.py                 resolve, run, print table and paths
  cli/main.py                        dispatch and return an exit code
```

`backends/__init__.py`, `metrics/__init__.py`, and `tasks/__init__.py` only import the concrete modules that must register. Split those imports if they cross 20 code lines.

Tests follow the same cap. One test module covers one behavior. They run on CPU. They do not download CLIP, Inception, or Diffusers weights. Library-call tests put a fake module in `sys.modules` and assert the keyword arguments (`mode`, directories, device, seed). A test that registers an extra name calls `unregister` before it finishes.

```
tests/registry/test_register.py
tests/registry/test_duplicate.py
tests/registry/test_missing.py
tests/registry/test_unregister.py
tests/tasks/test_core_suite.py
tests/tasks/test_duplicate_id.py
tests/tasks/test_relative_reference.py
tests/dummy/test_same_seed.py
tests/dummy/test_other_seed.py
tests/aggregate/test_mean_std.py
tests/aggregate/test_one_seed.py
tests/aggregate/test_skipped.py
tests/clip/test_formula.py
tests/cmmd/test_zero.py
tests/cmmd/test_known_pair.py
tests/distribution/test_folder_kwargs.py
tests/distribution/test_stats_kwargs.py
tests/distribution/test_seeded_call.py
tests/geneval/test_skipped.py
tests/diffusers/test_preset.py
tests/diffusers/test_call_kwargs.py
tests/diffusers/test_attention_name.py
tests/diffusers/test_missing_dependency.py
tests/runner/test_dummy_json_html.py
tests/runner/test_seed_mean.py
tests/runner/test_html_escape.py
tests/cli/test_list.py
tests/cli/test_unknown_suite.py
tests/cli/test_strict.py
tests/cli/test_console_script.py
```

## Metric definitions to preserve

These are the definitions the recommended decisions lock. Each one is stored in that metric's `protocol` dict. Published tables are comparable only after the number is checked against the reference implementation on the same dataset, resolution, and sample count. The bundled `core` suite is four synthetic prompts and four synthetic reference drawings. Its scores are a smoke test.

CLIP score, if D2 stays with Hessel et al. 2021:

- Model `openai/clip-vit-base-patch32`.
- Preprocess from that checkpoint's processor: shorter-side resize, center crop 224, CLIP mean and std.
- Text is the evaluation prompt, truncated to 77 tokens, with no added prefix.
- Score is the mean of `2.5 * max(cosine(image, text), 0)`.

CMMD, if D3 stays with the official JAX entry point:

- Model `openai/clip-vit-large-patch14-336`.
- Bicubic resize of the full image to 336×336, no center crop. Pixels are divided by 255 before the resize. CLIP mean and std are applied with the processor's own resize, crop, and rescale turned off.
- Embeddings are the vision projection. They are not L2-normalized again.
- Distance is the minimum-variance Gaussian RBF MMD from `google-research/cmmd/distance.py`: diagonal included, sigma 10, multiplied by 1000.

FID and KID, if D1 stays with clean-fid:

- The metric calls clean-fid. The package does not contain an Inception network.
- `mode="clean"` and, for FID, `model_name="inception_v3"`.
- clean-fid resizes each RGB image to 299×299 with PIL bicubic, per channel, in float, without quantizing back to uint8. diffeval writes the PNG and does not pre-resize.
- Folder mode passes the reference directory as `fdir1` and the generated directory as `fdir2`. `clean_fid_stats` passes the generated directory plus `dataset_name`, `dataset_res`, and `dataset_split`.
- KID uses clean-fid's degree-3 polynomial subset estimator (100 subsets, subset size at most 1000). The subset draw uses NumPy's global generator. The call seeds that generator with the evaluation seed and restores the previous state.
- `num_workers` is 0. Data-parallel feature extraction is on only when the metric device is CUDA.

GenEval v1 returns `skipped`. `details.by_tag` has the keys `single_object`, `two_object`, `counting`, `colors`, `position`, and `color_attr`, each null. The Mask2Former detector is not imported.

`core` uses seeds `[0, 1]` and 512×512 so a real pipeline has a usable smoke resolution and std is defined once a metric returns two values. FID, KID, and CMMD on four images are computed when the libraries are installed, and `details.warning` says the count is below published setups (FID often uses thousands of images; the CMMD paper uses COCO 30k).

The Diffusers preset for `black-forest-labs/FLUX.1-schnell` is 4 steps and guidance 0 when the CLI omits those flags (decision D10). Other model ids leave the pipeline's own defaults in place by omitting `num_inference_steps` and `guidance_scale`. A value passed on the CLI wins. `--attention` accepts `sdpa`, `xformers`, and `eager`. With no flag, the pipeline default stays and `attention_name` records it.

float16 and bfloat16 requested on CPU are loaded as float32. `dtype` in the results is the dtype actually used. `requested_dtype` keeps the flag.

## Packaging

- Source layout `src/diffeval`, Python `>=3.10`, Apache-2.0.
- Console script `diffeval` points at `cli.main`.
- Runtime dependencies start empty and grow only in the PR that first imports them: `pyyaml` with the suite loader, `pillow` with the dummy backend, `numpy` with CMMD.
- Extra `diffusers`: torch, diffusers, transformers, accelerate, safetensors.
- Extra `metrics`: torch, transformers, and the FID/KID library chosen in D1.
- Extras `geneval` and `video` exist so those stacks stay off the default install. v1 does not pin the Mask2Former detector or VBench, and the GenEval metric stays skipped.
- Extra `dev`: pytest.
- CI on Python 3.10, 3.11, and 3.12 installs the dev extra and runs pytest. The smoke command is added to CI in the PR that ships the `core` suite.

## Open decisions

The roadmap uses the recommended option. A different choice changes the body of the named modules and does not change the registry or the runner.

### D1. FID and KID library

Recommended: clean-fid, `mode="clean"`. The clean resizer is the one the clean-fid paper uses to match a JAX Inception reference, and one library covers FID and KID.

Alternative: torch-fidelity. It also avoids a homemade Inception and reports a KID mean and std from its own subsets. Resize and interpolation differ from clean-fid, so numbers from the two libraries are not interchangeable. Switching means rewriting `metrics/distribution/` and the FID/KID protocol text. The metric names stay `fid` and `kid`.

### D2. CLIP score scale and model

Recommended: Hessel et al. 2021, ViT-B/32, `2.5 * max(cosine, 0)`, raw prompt.

Alternative: the 0–100 form `100 * max(cosine, 0)`, often with ViT-L/14, which many diffusion papers print. Pick one and keep it in `metric_protocols`. The two scales must not be mixed in one column.

### D3. CMMD embedding normalization

Recommended: no extra L2 normalization, matching `google-research/cmmd/embedding.py` (scenic CLIP image embedding as returned). Sigma 10 was chosen for that scale.

Alternative: L2-normalize, as in the PyTorch port `sayakpaul/cmmd-pytorch`. That port will not match this package if the recommendation stands. The MMD function itself is the same minimum-variance estimator either way.

### D4. Suite file format

Recommended: YAML. It matches the usual benchmark-config style and keeps prompts readable.

Alternatives: JSON or TOML. The field names stay. `tasks/read_yaml.py` and `tasks/load_path.py` change. The registry does not.

### D5. CLI library

Recommended: argparse from the standard library, so the default install does not gain a CLI dependency. The parser is already split across three modules to fit the line cap.

Alternatives: click or typer. `cli/parser.py` and the two `run_parser_*.py` modules change. `main(argv) -> int` stays, so tests keep calling `main([...])`.

### D6. What the 20-line cap covers

Recommended: every `.py` file in `src/` and `tests/`. Docstrings, comments, and blank lines are outside the count. YAML, HTML, Markdown, `pyproject.toml`, and workflow YAML are outside the count because those formats do not split cleanly into 20-line pieces.

Alternative: count every text file. Workflow YAML and `pyproject.toml` would need a different layout.

### D7. HTML report

Recommended: one static `page.html` template and a Python filler that replaces placeholders. Table rows and figures are strings from their own modules. No template engine.

Alternative: Jinja or another engine. That adds a dependency and replaces `html_page.py`. The report contents stay the same.

### D8. How multiple seeds meet distribution metrics

Recommended: compute FID, KID, CMMD, and CLIP score on each seed's images, then report mean and sample std across seeds. That matches "multiple seeds, report mean/std" for every metric, and each seed stays reproducible on its own.

Alternative: pool every seed into one FID/KID/CMMD, and also store per-seed scores. The aggregate row would need a `pooled` field. Distribution metrics on a handful of images per seed are noisy either way; `details.warning` stays.

### D9. Standard deviation

Recommended: sample standard deviation, `ddof=1`, null when fewer than two successful seeds. `std_ddof` is recorded as `1`.

Alternative: population standard deviation, `ddof=0`. One-seed runs would show std 0, which looks like a measurement.

### D10. Sampler defaults

Recommended: `black-forest-labs/FLUX.1-schnell` uses 4 steps and guidance 0 when the flags are omitted, because that is the model card setting and it is the command in the quickstart. Any other pipeline omits the arguments so Diffusers uses its own defaults. CLI flags override the preset.

Alternative: never special-case a model id. The quickstart must pass `--steps 4 --guidance 0` for schnell. `presets.py` becomes empty or goes away.

### D11. GenEval and VBench in v1

Recommended: register `geneval` and return `skipped` with the tag schema. Do not register a fake `vbench` score. The `video` extra is only a packaging boundary. README says video scoring is later.

Alternative: do not register `geneval` until the detector exists. Suites cannot name it yet. The stub module goes away.

### D12. API backends

Recommended: v1 ships `dummy` and `diffusers` only. fal and Replicate implement `from_config`, `prepare`, `generate`, and `describe` later. No registered placeholder that fails on generate.

Alternative: register `fal` and `replicate` now and return a clear error from `generate`. That adds modules and list-command entries before the clients exist.

### D13. Reference images for `core`

Recommended: ship four small synthetic PNGs and point `reference_dir` at them. FID, KID, and CMMD have a folder to read when the metrics extra is installed. The protocol and the HTML page say the drawings are not COCO.

Alternative: `core` has no reference directory. Those three metrics skip until a suite sets `reference_dir` or `clean_fid_stats`. The smoke command still writes JSON and HTML.

### D14. Strict exit

Recommended: `--strict` is off by default. A smoke run with the metrics extra missing exits 0 and records `skipped`. `--strict` exits 2 after writing the report.

Alternative: strict by default. The documented dummy command would fail until the metrics extra and weights are present.
