"""One CLIP vision batch, L2-normalized like the official CMMD."""

_CACHE = {}


def load_vision(model_name: str):
    if model_name in _CACHE:
        return _CACHE[model_name]
    try:
        from transformers import CLIPImageProcessor, CLIPModel
    except ImportError:
        return None
    model = CLIPModel.from_pretrained(model_name)
    model.eval()
    processor = CLIPImageProcessor.from_pretrained(model_name)
    processor.do_resize = processor.do_center_crop = processor.do_rescale = False
    _CACHE[model_name] = (model, processor)
    return _CACHE[model_name]


def embed_batch(model, processor, images, device):
    import torch
    pixels = processor(images=images, return_tensors="pt")["pixel_values"].to(device)
    with torch.no_grad():
        embeds = model.visual_projection(model.vision_model(pixel_values=pixels).pooler_output)
        return (embeds / embeds.norm(dim=-1, keepdim=True)).detach().cpu().numpy()
