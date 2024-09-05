from flask import Flask, request, jsonify
from transformers import T5Tokenizer, TFT5ForConditionalGeneration

app = Flask(__name__)
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = TFT5ForConditionalGeneration.from_pretrained('./halthia_model')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/generate", methods=["POST"])
def generate_response():
    input_text = request.json['input_text']
    input_encoding = tokenizer.encode(input_text, return_tensors='tf', max_length=32, truncation=True)
    generated_ids = model.generate(input_encoding, max_length=32, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return jsonify({'generated_text': generated_text})