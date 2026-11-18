"""Shared FID and KID protocol."""

PROTOCOL = {
    "library": "clean-fid",
    "mode": "clean",
    "model": "inception_v3",
    "resize": "clean-fid resizes each RGB image to 299x299 with PIL bicubic per channel in float and does not quantize back to uint8",
    "pre_resize": "diffeval does not pre-resize",
    "num_workers": 0,
    "dataparallel": "only when the metric device is cuda",
    "kid": "degree-3 polynomial, 100 subsets, subset size at most 1000",
}
