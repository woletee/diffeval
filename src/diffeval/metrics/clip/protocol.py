"""CLIPScore definition text."""

PROTOCOL = {
    "paper": "Hessel et al. 2021",
    "model": "openai/clip-vit-base-patch32",
    "weight": 2.5,
    "crop": "shorter-side resize, center crop 224",
    "text": "raw prompt, truncated to 77 tokens, no prefix",
    "formula": "mean of 2.5 * max(cosine, 0)",
}
