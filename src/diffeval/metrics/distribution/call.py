"""Call clean-fid for FID or KID."""

from diffeval.metrics.count_warning import count_warning
from diffeval.metrics.distribution.kwargs_folder import distribution_kwargs
from diffeval.metrics.distribution.seed_numpy import seeded
from diffeval.metrics.fid.guard import fid_ready
from diffeval.metrics.images import list_images
from diffeval.metrics.ok import ok
from diffeval.metrics.skipped import skipped


def score_distribution(kind, context, protocol, model_name=None):
    reason = fid_ready(context)
    if reason:
        return skipped(kind, reason, False, protocol)
    try:
        from cleanfid import fid as clean_fid
    except ImportError:
        return skipped(kind, "metrics extra is not installed", False, protocol)
    fn = clean_fid.compute_fid if kind == "fid" else clean_fid.compute_kid
    kwargs = distribution_kwargs(context, model_name)
    value = seeded(context.seed, lambda: fn(**kwargs))
    warning = count_warning(len(list_images(context.generated_dir)))
    return ok(kind, float(value), False, protocol, {} if warning is None else {"warning": warning})
