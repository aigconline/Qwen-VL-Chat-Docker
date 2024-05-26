import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from flask import Flask, request, jsonify, json, make_response
import uuid
import base64
import os
 
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

app = Flask(__name__)
 
@app.route('/qwen/vl/chat', methods=['POST'])
def qwen_chat():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON in request body'}), 400

    text = data.get('text', None)
    if not text:
        return jsonify({'error': 'Array parameter is required'}), 400
    chat_list = [{'text': text}]

    images = data.get('image', [])
    for i in range(0, len(images)):
        chat_list.insert(i, {"image": images[i]})

    query = tokenizer.from_list_format(chat_list)
    history = data.get('history', None)

    response, history = model.chat(tokenizer, query=query, history=history)

    image_base64 = None
    if response.startswith("<ref>"):
        image = tokenizer.draw_bbox_on_latest_picture(response, history)
        new_image_path = "/tmp/" + str(uuid.uuid4()) + ".jpg"
        image.save(new_image_path)
        with open(new_image_path, 'rb') as img_obj:
            base64_data = base64.b64encode(img_obj.read())
            image_base64 = str(base64_data,"utf-8")
            os.remove(new_image_path)  

    result_response = {"result": response, "history": history, "image": image_base64}
    json_data = json.dumps(result_response, ensure_ascii=False)
    resp = make_response(json_data)
    resp.headers['Content-Type'] = 'application/json'

    return resp
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
