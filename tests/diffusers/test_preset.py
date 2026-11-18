"""Schnell preset, a CLI override, and an unknown model id."""

from types import SimpleNamespace

from diffeval.backends.diffusers.describe import describe
from diffeval.backends.diffusers.presets import SCHNELL
from diffeval.backends.diffusers.sampling import sampling
from diffeval.cli.config import backend_name


def test_schnell_preset_and_cli_step():
    bare = sampling({"pipeline": SCHNELL})
    stepped = sampling({"pipeline": SCHNELL, "steps": 2})
    assert bare["steps"] == 4 and bare["guidance"] == 0.0 and bare["steps_source"] == bare["guidance_source"] == "preset"
    assert stepped["steps"] == 2 and stepped["steps_source"] == "cli" and stepped["guidance"] == 0.0 and stepped["guidance_source"] == "preset"


def test_unknown_model_uses_pipeline_default():
    found = sampling({"pipeline": "org/other"})
    assert found["steps"] is None and found["guidance"] is None and found["steps_source"] == found["guidance_source"] == "pipeline-default"


def test_describe_and_pipeline_flag():
    config = {"pipeline": SCHNELL, "dtype": "float16", "batch_size": 1}
    state = {"sampling": sampling(config), "device": "cpu", "dtype_text": "float32", "attention": "sdpa"}
    info = describe(config, state)
    args = SimpleNamespace(backend=None, pipeline=SCHNELL)
    assert info["dtype"] == "float32" and info["requested_dtype"] == "float16" and info["steps_source"] == "preset" and info["device"] == "cpu" and info["attention_backend"] == "sdpa"
    assert backend_name(args) == "diffusers" and info["guidance"] == 0.0 and info["guidance_source"] == "preset"
