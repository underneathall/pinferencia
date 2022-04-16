import torch

from pinferencia import Server

# load tokenizer
tokenizer = torch.hub.load(
    "huggingface/pytorch-transformers",
    "tokenizer",
    "bert-base-cased",
)
# load masked model
masked_lm_model = torch.hub.load(
    "huggingface/pytorch-transformers",
    "modelForMaskedLM",
    "bert-base-cased",
)


def predict(input_text):
    # tokenize the input text
    tokens = tokenizer(input_text)

    # get all the mask index
    mask_index = [
        i
        for i, token_id in enumerate(tokens["input_ids"])
        if token_id == tokenizer.mask_token_id
    ]

    # convert the input ids and type ids to tensor
    segments_tensors = torch.tensor([tokens["token_type_ids"]])
    tokens_tensor = torch.tensor([tokens["input_ids"]])

    # run predictions
    with torch.no_grad():
        predictions = masked_lm_model(
            tokens_tensor, token_type_ids=segments_tensors
        )

    # pick the most likely predictions
    pred_tokens = torch.argmax(predictions[0][0], dim=1)

    # replace the initail input text's mask with predicted text
    for i in mask_index:
        tokens["input_ids"][i] = pred_tokens[i]
    return tokenizer.decode(tokens["input_ids"], skip_special_tokens=True)


service = Server()
service.register(model_name="transformer", model=predict)
