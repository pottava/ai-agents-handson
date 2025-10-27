from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

raw_inputs = [
    "今日は雨が凄いので外出したくないな。",
    "今日は天気が良いので外に出かけたいな。",
]

tokenized = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(tokenized)
