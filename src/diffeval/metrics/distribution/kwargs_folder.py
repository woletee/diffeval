"""Folder-mode arguments for clean-fid."""

from diffeval.metrics.distribution.kwargs_stats import stats_kwargs


def folder_kwargs(reference, generated, device, batch_size, model_name=None) -> dict:
    body = {"fdir1": str(reference), "fdir2": str(generated), "mode": "clean", "num_workers": 0, "batch_size": int(batch_size), "device": device, "verbose": False, "use_dataparallel": device == "cuda"}
    if model_name:
        body["model_name"] = model_name
    return body


def distribution_kwargs(context, model_name=None) -> dict:
    if context.clean_fid_stats:
        return stats_kwargs(context.generated_dir, context.clean_fid_stats, context.device, context.batch_size, model_name)
    return folder_kwargs(context.reference_dir, context.generated_dir, context.device, context.batch_size, model_name)
