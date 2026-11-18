<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://diffeval.vercel.app/assets/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://diffeval.vercel.app/assets/logo-light.svg">
  <img alt="diffeval" src="https://diffeval.vercel.app/assets/logo-light.svg" width="240">
</picture>

# diffeval: A Framework for Diffusion Model Evaluation

A fixed prompt and seed suite, scored the same way on every model.

**Website: [diffeval.vercel.app](https://diffeval.vercel.app)**

[![Website](https://img.shields.io/badge/website-diffeval.vercel.app-000000?style=flat&colorA=000000&colorB=000000)](https://diffeval.vercel.app)
[![CI](https://img.shields.io/github/actions/workflow/status/woletee/diffeval/ci.yml?style=flat&label=CI&colorA=000000&colorB=000000)](https://github.com/woletee/diffeval/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-000000?style=flat&colorA=000000&colorB=000000)](https://github.com/woletee/diffeval/blob/main/pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache--2.0-000000?style=flat&colorA=000000&colorB=000000)](https://github.com/woletee/diffeval/blob/main/LICENSE)

<p>
  <a href="https://diffeval.vercel.app">Website</a>
  ·
  <a href="#quickstart">Quickstart</a>
  ·
  <a href="#metrics">Metrics</a>
  ·
  <a href="#suites">Suites</a>
  ·
  <a href="docs/BENCHMARKS.md">Benchmarks</a>
  ·
  <a href="docs/DESIGN.md">Design</a>
</p>

</div>

diffeval is an evaluation harness for text-to-image diffusion models, in the spirit of [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness). A suite fixes the prompts, seeds and resolution; a backend generates the images; every metric scores each seed; the runner reports mean ± std.

- **Pluggable.** Suites, metrics and backends register by name.
- **Light.** The base install is PyYAML, Pillow and NumPy. Torch and friends are optional extras.
- **Honest.** A metric that can't run is marked `skipped` with the reason, never silently dropped.
- **Traceable.** `results.json` records the suite, model settings, package versions and each metric's protocol.

## Results

`cmmd` reproduces the [cmmd-pytorch](https://github.com/sayakpaul/cmmd-pytorch) reference value (7.696) exactly. Below: the first N COCO-30k captions, seed 2024.

| Model | Steps | Hardware | Captions | `clip_score` | `cmmd` | Published CMMD (30k) |
| --- | --- | --- | --- | --- | --- | --- |
| SD 1.5 | 50 | T4, fp16 | 1,000 | 0.774 | 0.615 | 0.582 |
| SD-Turbo | 1 | CPU, fp32 | 500 | 0.785 | 0.683 | — |

SD 1.5 sits slightly above the published value because of the smaller caption set and the safety checker's black images. Commands to reproduce: [docs/BENCHMARKS.md](docs/BENCHMARKS.md).

## Install

```bash
pip install diffeval                         # CLI only
pip install "diffeval[diffusers,metrics]"    # generate and score
```

| Extra | For |
| --- | --- |
| `diffusers` | the `diffusers` backend |
| `metrics` | `clip_score`, `cmmd`, `fid`, `kid` |
| `geneval2` | the `geneval2` metric (Qwen3-VL-8B judge, ~24 GB GPU) |
| `benchmarks` | downloading COCO-30k reference images |
| `dev` | tests |

Python 3.10+.

## Quickstart

```bash
# CPU smoke test, no downloads
diffeval run --backend dummy --suite core

# a real model
diffeval run --pipeline stabilityai/sd-turbo --suite core --steps 1 --guidance 0

# list suites, metrics and backends
diffeval list tasks
diffeval list metrics
diffeval list backends
```

Each run writes `outputs/<timestamp>-<suite>-<backend>/` with the images, `results.json`, `report.md` and `report.html`. Add `--strict` to exit 2 unless every metric is `ok`. See `diffeval run --help` for all options.

> [!NOTE]
> `core` is a smoke suite with four synthetic prompts, not a benchmark.

## Metrics

| Metric | Better | What it is |
| --- | :---: | --- |
| `clip_score` | ↑ | CLIP ViT-B/32 prompt–image similarity (Hessel et al. 2021) |
| `cmmd` | ↓ | CLIP-embedding MMD (Jayasumana et al. 2024); matches cmmd-pytorch |
| `fid` | ↓ | clean-fid, Inception-v3 |
| `kid` | ↓ | clean-fid, polynomial kernel |
| `geneval2` | ↑ | [GenEval 2](https://github.com/facebookresearch/GenEval2) Soft-TIFA with a Qwen3-VL-8B judge |
| `geneval` | ↑ | placeholder, always `skipped` |

`cmmd`, `fid` and `kid` need reference images. For GenEval 2, build the prompt suite with `diffeval-geneval2 --out DIR` (the data is CC BY-NC 4.0 and downloaded, not shipped). Exact formulas are in [docs/DESIGN.md](docs/DESIGN.md).

## Custom suites

```yaml
name: shapes
seeds: [0, 1]
metrics: [clip_score]
prompts:
  - {id: red_cube, prompt: a red cube}
  - {id: blue_sphere, prompt: a blue sphere}
```

```bash
diffeval run --pipeline stabilityai/sd-turbo --suite shapes.yaml
```

## Extending

Add a module that registers into `TASKS`, `METRICS` or `BACKENDS` and import it from the package `__init__.py`:

```python
from diffeval.metrics.ok import ok
from diffeval.registry.register import register
from diffeval.registry.tables import METRICS

@register(METRICS, "example")
class Example:
    name = "example"
    description = "What the number means."
    higher_is_better = True
    requires_references = False
    protocol = {"formula": "..."}

    def compute(self, samples, context):
        return ok(self.name, 0.0, self.higher_is_better, self.protocol)
```

Interfaces and the module tree are in [docs/DESIGN.md](docs/DESIGN.md).

## Contributing

```bash
pip install -e ".[dev]" && pytest
```

Every `.py` file in `src/` and `tests/` is capped at 20 lines of code.

## License

Apache-2.0
