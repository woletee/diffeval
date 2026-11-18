"""diffeval-check-cmmd: score the cmmd-pytorch samples and expect 7.696."""

import argparse
import sys
import tempfile
from pathlib import Path

from diffeval.bench.cmmd_samples import cmmd_samples

EXPECTED = 7.696


def main(argv=None) -> int:
    argparse.ArgumentParser(prog="diffeval-check-cmmd", description=f"Score the six cmmd-pytorch sample images and expect CMMD {EXPECTED}.").parse_args(argv)
    from diffeval.metrics.cmmd import embed_batch
    from diffeval.metrics.cmmd.embed_paths import embed_dir
    from diffeval.metrics.cmmd.mmd import mmd
    loaded = embed_batch.load_vision("openai/clip-vit-large-patch14-336")
    if loaded is None:
        print("diffeval-check-cmmd needs the metrics extra: pip install 'diffeval[metrics]'", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as tmp:
        ref_dir, gen_dir = cmmd_samples(Path(tmp))
        value = round(mmd(embed_dir(*loaded, ref_dir, "cpu"), embed_dir(*loaded, gen_dir, "cpu")), 3)
    print(f"CMMD {value} (expected {EXPECTED})")
    return 0 if abs(value - EXPECTED) < 0.001 else 1
