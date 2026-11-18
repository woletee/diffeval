"""Load the Qwen3-VL judge as the reference does, once per model id."""

MODEL = "Qwen/Qwen3-VL-8B-Instruct"
_CACHE = {}


def load_judge(model_id: str = MODEL):
    if model_id in _CACHE:
        return _CACHE[model_id]
    try:
        from transformers import AutoProcessor, Qwen3VLForConditionalGeneration
    except ImportError:
        return None
    processor = AutoProcessor.from_pretrained(model_id, torch_dtype="auto", device_map="auto")
    model = Qwen3VLForConditionalGeneration.from_pretrained(model_id, dtype="auto", device_map="auto")
    _CACHE[model_id] = (processor, model)
    return _CACHE[model_id]
