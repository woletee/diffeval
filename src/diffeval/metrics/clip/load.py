"""Load CLIPModel and CLIPProcessor."""

_CACHE = {}


def load_clip(model_name: str):
    if model_name in _CACHE:
        return _CACHE[model_name]
    try:
        from transformers import CLIPModel, CLIPProcessor
    except ImportError:
        return None
    model = CLIPModel.from_pretrained(model_name)
    model.eval()
    processor = CLIPProcessor.from_pretrained(model_name)
    _CACHE[model_name] = (model, processor)
    return _CACHE[model_name]
