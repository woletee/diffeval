"""Prompt and negative prompt arguments."""


def prompt_kwargs(requests) -> dict:
    prompts = [item.prompt for item in requests]
    body = {"prompt": prompts[0] if len(requests) == 1 else prompts}
    negatives = [item.negative_prompt for item in requests]
    if any(negatives):
        filled = [text or "" for text in negatives]
        body["negative_prompt"] = filled[0] if len(requests) == 1 else filled
    return body
