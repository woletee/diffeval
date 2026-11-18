# Benchmarks

diffeval is checked against published numbers. The anchor is the COCO-30k CMMD table from [cmmd-pytorch](https://github.com/sayakpaul/cmmd-pytorch). That project publishes everything needed to repeat it: the 30,000 COCO-2014 val captions, the reference CLIP embeddings, and the generation settings. A diffeval run that follows the same protocol should land near the published value.

| Model | Steps | Size | Guidance | Published CMMD |
| --- | --- | --- | --- | --- |
| `stable-diffusion-v1-5/stable-diffusion-v1-5` | 50 | 512 | pipeline default | 0.582 |
| `stabilityai/sdxl-turbo` | 1 | 512 | 0 | 0.548 |
| `stabilityai/stable-diffusion-xl-base-1.0` | 30 | 1024 | pipeline default | 0.696 |
| `segmind/SSD-1B` | 30 | 1024 | pipeline default | 0.669 |
| `PixArt-alpha/PixArt-XL-2-1024-MS` | 20 | 1024 | pipeline default | 1.140 |

cmmd-pytorch generated in float16 on CUDA with seed 2024. The SD 1.5 row was published under the old id `runwayml/stable-diffusion-v1-5`, which now lives at `stable-diffusion-v1-5/stable-diffusion-v1-5`.

`clip_score`, `fid`, and `kid` have no published value under this exact protocol, so the table reports them without a comparison.

## Results so far

| Model | Hardware | Captions | `clip_score` | `cmmd` | Published CMMD (30k) |
| --- | --- | --- | --- | --- | --- |
| `stable-diffusion-v1-5/stable-diffusion-v1-5`, 50 steps | NVIDIA T4, float16 | 1,000 | 0.774 | 0.615 | 0.582 |
| `stabilityai/sd-turbo`, 1 step, guidance 0 | CPU, float32 | 500 | 0.785 | 0.683 | not published |

`diffeval-check-cmmd` printed 7.696 on both machines. SDXL-Turbo, SDXL, SSD-1B, and PixArt-α have not been run yet.

The SD 1.5 safety checker replaces images it flags with black images. Those stay in the sample and raise CMMD a little.

## GPU run

These commands run on a machine with a CUDA GPU.

### 1. Install

```bash
pip install "diffeval[diffusers,metrics]"
```

Requirements:

- PyTorch 2.6 or newer with CUDA. Recent transformers refuse to load the CLIP `.bin` weights on older PyTorch (CVE-2025-32434). If another project needs an older PyTorch, give diffeval its own virtual environment.
- About 25 GB of free disk: the environment, CLIP ViT-L/14 (1.7 GB), each model's weights, and the images. Set `HF_HOME` to a disk with room if the home directory is small.

On Google Colab, pick **Runtime → Change runtime type → T4 GPU** first, and check that `torch.cuda.is_available()` prints `True`.

### 2. Check CMMD against the known value

```bash
diffeval-check-cmmd
```

It must print `CMMD 7.696 (expected 7.696)`. Stop if it does not.

### 3. Build the suite

```bash
diffeval-coco30k --out benchmarks/coco30k
```

This downloads the captions and `ref_embs_coco_30k.npy` (92 MB) and writes `benchmarks/coco30k/suite.yaml` with `clip_score` and `cmmd`.

FID and KID are optional. They need the 30,000 reference images, about 5 GB:

```bash
pip install "diffeval[benchmarks]"
diffeval-coco30k-images --out benchmarks/coco30k/images
diffeval-coco30k --out benchmarks/coco30k --reference-images benchmarks/coco30k/images
```

### 4. Run each model

Each command writes one output folder. `--variant fp16` downloads only the half-precision weights, about half the size. `--batch-size` only changes speed. Lower it if the GPU runs out of memory. A free T4 takes about 7 seconds per image for SD 1.5 at 50 steps.

```bash
diffeval run --suite benchmarks/coco30k/suite.yaml --pipeline stable-diffusion-v1-5/stable-diffusion-v1-5 --variant fp16 --steps 50 --dtype float16 --device cuda --batch-size 16 --output outputs/sd15
```

```bash
diffeval run --suite benchmarks/coco30k/suite.yaml --pipeline stabilityai/sdxl-turbo --variant fp16 --steps 1 --guidance 0 --dtype float16 --device cuda --batch-size 16 --output outputs/sdxl-turbo
```

```bash
diffeval run --suite benchmarks/coco30k/suite.yaml --pipeline stabilityai/stable-diffusion-xl-base-1.0 --variant fp16 --steps 30 --width 1024 --height 1024 --dtype float16 --device cuda --batch-size 4 --output outputs/sdxl
```

```bash
diffeval run --suite benchmarks/coco30k/suite.yaml --pipeline segmind/SSD-1B --variant fp16 --steps 30 --width 1024 --height 1024 --dtype float16 --device cuda --batch-size 4 --output outputs/ssd-1b
```

```bash
diffeval run --suite benchmarks/coco30k/suite.yaml --pipeline PixArt-alpha/PixArt-XL-2-1024-MS --steps 20 --width 1024 --height 1024 --dtype float16 --device cuda --batch-size 4 --output outputs/pixart
```

For a quicker first pass, build the suite with `--limit 5000` and run the same commands. CMMD holds up well with fewer images; FID does not.

### 5. Make the table

```bash
diffeval-table outputs/*/results.json
```

Send back the printed table and each `outputs/<model>/results.json`. The images are not needed.

## CPU run

`diffeval-coco30k --limit N` builds a smaller suite for a CPU. On a laptop CPU, `stabilityai/sd-turbo` at one step takes about five seconds per 512 image, and a 50-step model takes minutes per image. CPU rows use a few hundred captions, and the table says so.

## GenEval 2 prompts

```bash
pip install "diffeval[diffusers,geneval2]"
diffeval-geneval2 --out benchmarks/geneval2
diffeval run --pipeline stabilityai/sdxl-turbo --variant fp16 --suite benchmarks/geneval2/suite.yaml
```

`diffeval-geneval2` downloads the 800 [GenEval 2](https://github.com/facebookresearch/GenEval2) prompts from a pinned commit and writes `suite.yaml`. Each prompt keeps its questions, skills, and atom count in `meta`. `--limit N` keeps the first N prompts, `--size` sets the image size (default 512), and `--seed` sets the seed (default 0). The GenEval 2 data is CC BY-NC 4.0, so diffeval downloads it instead of shipping it.

The suite scores `geneval2`: Soft-TIFA with the Qwen3-VL-8B judge, the method the GenEval 2 paper reports. The judge is about 17 GB in its default precision, so it needs a GPU with about 24 GB (an L4 or A100, not a T4). `results.json` also keeps the arithmetic-mean score, the per-skill and per-atom-count scores, and every question score. The image model and the judge both load in the same run, so the GPU needs room for both.

### Check geneval2 against the reference

`diffeval-check-geneval2` rescores a finished `geneval2` run with the official GenEval 2 `evaluation.py`, downloaded from the same pinned commit, on the same PNG files. It then compares every question score. It passes when no question differs by more than `--tolerance` (default `1e-4`), and prints both Soft-TIFA GM totals. The reference loads the judge again in its own process, so run it after `diffeval run` finishes. A 100-prompt run is enough for the check and takes about half the time of the full 800.

```bash
pip install "diffeval[diffusers,geneval2]" scipy tqdm
diffeval-geneval2 --out benchmarks/geneval2-100 --limit 100
diffeval run --pipeline stable-diffusion-v1-5/stable-diffusion-v1-5 --variant fp16 --suite benchmarks/geneval2-100/suite.yaml --output outputs/geneval2-check-sd15
diffeval-check-geneval2 --run outputs/geneval2-check-sd15
```

The reference script and data are CC BY-NC 4.0. diffeval downloads them into `<run>/geneval2-check/` and does not ship them. On Colab, pick an L4 or A100 runtime: the judge does not fit on a T4.
