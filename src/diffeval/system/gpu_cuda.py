"""CUDA device name, index, count, and memory."""


def gpu_cuda(torch):
    if not torch.cuda.is_available():
        return None
    index = torch.cuda.current_device()
    props = torch.cuda.get_device_properties(index)
    return {"name": props.name, "index": index, "count": torch.cuda.device_count(), "total_memory": props.total_memory}
