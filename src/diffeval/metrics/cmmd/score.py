"""Reference folder or .npy against generated PNGs."""

from diffeval.metrics.cmmd.embed_batch import load_vision
from diffeval.metrics.cmmd.embed_paths import paired
from diffeval.metrics.cmmd.mmd import mmd
from diffeval.metrics.cmmd.protocol import PROTOCOL
from diffeval.metrics.count_warning import count_warning
from diffeval.metrics.ok import ok
from diffeval.metrics.skipped import skipped


def score_cmmd(context):
    if context.reference_dir is None and context.cmmd_ref_embed is None:
        return skipped("cmmd", "reference set is missing", False, PROTOCOL)
    loaded = load_vision(PROTOCOL["model"])
    if loaded is None:
        return skipped("cmmd", "metrics extra is not installed", False, PROTOCOL)
    model, processor = loaded
    model.to(context.device)
    generated, reference = paired(context, model, processor)
    if generated is None or reference is None:
        return skipped("cmmd", "reference set is missing", False, PROTOCOL)
    warning = count_warning(len(generated))
    return ok("cmmd", float(mmd(reference, generated)), False, PROTOCOL, {} if warning is None else {"warning": warning})
