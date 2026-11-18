"""CMMD definition text."""

PROTOCOL = {
    "paper": "Jayasumana et al. 2024",
    "model": "openai/clip-vit-large-patch14-336",
    "resize": "bicubic resize of the 8-bit image to 336 (PIL), then divided by 255",
    "crop": "center square crop",
    "embeddings": "vision projection, L2-normalized",
    "check": "cmmd-pytorch sample folders give 7.696",
    "distance": "minimum-variance RBF MMD, sigma 10, scale 1000, diagonal included",
}
