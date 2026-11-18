"""The suite mapping for the first N COCO-30k captions."""

from diffeval.bench.coco30k_files import EMB_NAME


def coco30k_suite(captions: list[str], seed: int, reference_images=None) -> dict:
    name = "coco30k" if len(captions) >= 30000 else f"coco30k-{len(captions)}"
    suite = {"name": name, "description": f"cmmd-pytorch COCO-30k captions (COCO 2014 val), first {len(captions)}"}
    suite.update(seeds=[seed], width=512, height=512, cmmd_ref_embed=EMB_NAME)
    metrics = ["clip_score", "cmmd"]
    if reference_images is not None:
        suite["reference_dir"] = str(reference_images)
        metrics += ["fid", "kid"]
    suite["metrics"] = metrics
    suite["prompts"] = [{"id": f"c{index:05d}", "prompt": text} for index, text in enumerate(captions)]
    return suite
