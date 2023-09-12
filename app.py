from flask import Flask, render_template, request, jsonify
import json
import requests
import io
from io import BytesIO
import base64
from PIL import Image, PngImagePlugin
import gzip
from translate import Translator

app = Flask(__name__)


def generate_image(prompt,width,height):
    url = "http://192.168.0.206:7860"
    payload = {
        "prompt": prompt,
        "negative_prompt": "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation",
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "batch_size": 1,
        "n_iter": 1,
        "steps": 25,
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "restore_faces": "false",
        "tiling": "false",
        "do_not_save_samples": "false",
        "do_not_save_grid": "false",
        "eta": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {"sd_model_checkpoint": "realisticVisionV20_v20.safetensors [c0d1994c73]"},
        "override_settings_restore_afterwards": "true",
        "sampler_index": "DPM++ SDE Karras",
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    base64_str = r['images'][0].split(",", 1)[0]

    return base64_str

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate():
    prompt = request.json['prompt']
    width = request.json['width']
    height = request.json['height']
    print("start to generate_image")
    image_data = generate_image(prompt,width,height)
    return jsonify({"image": image_data})

if __name__ == '__main__':
    app.run()