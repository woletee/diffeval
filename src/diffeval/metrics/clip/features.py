"""L2-normalized CLIP image and text features."""


def _norm(tensor):
    return tensor / tensor.norm(dim=-1, keepdim=True)


def features(model, processor, images, texts, device):
    import torch
    batch = processor(text=texts, images=images, return_tensors="pt", padding=True, truncation=True, max_length=77)
    batch = batch.to(device)
    with torch.no_grad():
        output = model(**batch)
    return _norm(output.image_embeds), _norm(output.text_embeds)
