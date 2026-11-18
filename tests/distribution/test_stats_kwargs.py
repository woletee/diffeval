"""Stats mode passes dataset fields and no second folder."""

import sys
import types

from diffeval.metrics.fid.metric import Fid
from diffeval.metrics.kid.metric import Kid
from diffeval.types.context import EvalContext


def test_stats_kwargs(tmp_path):
    calls = []
    fid_mod = types.ModuleType("cleanfid.fid")
    fid_mod.compute_fid = lambda **kw: calls.append(kw) or 3.0
    fid_mod.compute_kid = lambda **kw: calls.append(kw) or 4.0
    sys.modules["cleanfid"] = types.ModuleType("cleanfid"); sys.modules["cleanfid"].fid = fid_mod
    gen = tmp_path / "gen"
    gen.mkdir() or [(gen / name).write_bytes(b"x") for name in ("a.png", "b.png")]
    context = EvalContext(gen, None, "cuda", 2, {"dataset_name": "coco", "dataset_res": 256, "dataset_split": "custom"}, None, 4)
    assert Fid().compute([], context).value == 3.0 and Kid().compute([], context).value == 4.0
    fid_kw, kid_kw = calls
    assert fid_kw["fdir1"] == kid_kw["fdir1"] == str(gen) and "fdir2" not in fid_kw and "fdir2" not in kid_kw and fid_kw["use_dataparallel"] is kid_kw["use_dataparallel"] is True
    assert fid_kw["dataset_name"] == "coco" and fid_kw["dataset_res"] == 256 and fid_kw["dataset_split"] == "custom" and fid_kw["mode"] == "clean" and fid_kw["num_workers"] == 0
    assert fid_kw["model_name"] == "inception_v3" and "model_name" not in kid_kw and kid_kw["mode"] == "clean"
    sys.modules.pop("cleanfid", None)
