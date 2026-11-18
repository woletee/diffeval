"""Folder mode passes clean-fid folder arguments."""

import sys
import types

from diffeval.metrics.fid.metric import Fid
from diffeval.metrics.kid.metric import Kid
from diffeval.types.context import EvalContext


def test_folder_kwargs(tmp_path):
    calls = []
    fid_mod = types.ModuleType("cleanfid.fid")
    fid_mod.compute_fid = lambda **kw: calls.append(("fid", kw)) or 1.0
    fid_mod.compute_kid = lambda **kw: calls.append(("kid", kw)) or 2.0
    sys.modules["cleanfid"] = types.ModuleType("cleanfid"); sys.modules["cleanfid"].fid = fid_mod
    ref, gen = tmp_path / "ref", tmp_path / "gen"
    make = lambda folder: folder.mkdir() or [(folder / name).write_bytes(b"x") for name in ("a.png", "b.png")]
    make(ref), make(gen)
    context = EvalContext(gen, ref, "cpu", 1, None, None, 8)
    assert Fid().compute([], context).value == 1.0 and Kid().compute([], context).value == 2.0
    fid_kw, kid_kw = calls[0][1], calls[1][1]
    assert [fid_kw[key] for key in ("mode", "fdir1", "fdir2", "num_workers", "model_name", "use_dataparallel")] == ["clean", str(ref), str(gen), 0, "inception_v3", False]
    assert [kid_kw[key] for key in ("mode", "fdir1", "fdir2", "num_workers", "use_dataparallel")] == ["clean", str(ref), str(gen), 0, False] and "model_name" not in kid_kw
    sys.modules.pop("cleanfid", None)
