"""Ask the judge one question about one image: the argmax token and the accepted-answer probability."""

from diffeval.metrics.geneval2.judge_tokens import answer_prob, first_token_ids

GENERATE = {"max_new_tokens": 1, "do_sample": False, "output_scores": True, "return_dict_in_generate": True}


def messages(image, text: str) -> list:
    return [{"role": "user", "content": [{"type": "image", "image": image}, {"type": "text", "text": text}]}]


def ask(processor, model, image, text: str, answers: list[str]):
    import torch

    chat = processor.apply_chat_template(messages(image, text), tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt")
    outputs = model.generate(**chat.to(model.device), **GENERATE)
    probs = torch.nn.functional.softmax(outputs.scores[0], dim=-1)
    prob = answer_prob(probs[0], first_token_ids(processor.tokenizer, answers))
    return processor.batch_decode([torch.argmax(probs)])[0], prob
