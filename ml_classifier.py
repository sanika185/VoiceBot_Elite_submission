from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch

# Must match label2id mapping from training
id2label = {
    0: "Electricity",
    1: "Garbage",
    2: "Noise Pollution",
    3: "Road",
    4: "Water Supply"
}

# Load model and tokenizer from saved path
model = XLMRobertaForSequenceClassification.from_pretrained("models/complaint_classifier")
tokenizer = XLMRobertaTokenizer.from_pretrained("models/complaint_classifier")

def classify_complaint(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred = torch.argmax(probs).item()
    confidence = probs[0][pred].item() * 100
    return id2label[pred], confidence
