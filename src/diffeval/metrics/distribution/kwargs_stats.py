"""Stats-mode arguments for clean-fid."""


def stats_kwargs(generated, stats, device, batch_size, model_name=None) -> dict:
    body = {"fdir1": str(generated), "dataset_name": stats["dataset_name"], "dataset_res": stats["dataset_res"], "dataset_split": stats["dataset_split"], "mode": "clean", "num_workers": 0, "batch_size": int(batch_size), "device": device, "verbose": False, "use_dataparallel": device == "cuda"}
    if model_name:
        body["model_name"] = model_name
    return body
