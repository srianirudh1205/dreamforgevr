import os
import json
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file('index.html')

@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return app.send_static_file('dashboard.html')

@app.route("/house.json", methods=["GET"])
def get_house_data():
    if os.path.exists("house.json"):
        return send_file("house.json", mimetype='application/json')
    return jsonify({"error": "house.json not found"}), 404

@app.route("/parse-blueprint", methods=["POST"])
def parse_blueprint():
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY environment variable not set"}), 500

    if 'blueprint' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['blueprint']
    img_bytes = file.read()
    base64_img = base64.b64encode(img_bytes).decode('utf-8')

    prompt = (
        "Extract all rooms from this architectural blueprint. Return ONLY valid JSON matching this schema: "
        "{'rooms':[{'id', 'name', 'width', 'depth', 'height', 'position':{'x','y','z'}, 'material', 'color', 'costPerSqft'}]}. "
        "Dimensions in metres, Indian ₹/sqft costs. "
        "Assume standard materials. Arrange positions nicely in X space."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response_data = response.json()
        
        json_str = response_data['choices'][0]['message']['content']
        parsed_data = json.loads(json_str)

        with open("house.json", "w") as f:
            json.dump(parsed_data, f, indent=2)

        return jsonify({"status": "success", "message": "Blueprint parsed", "data": parsed_data})
    except Exception as e:
        return jsonify({"error": "Blueprint parsing failed", "detail": str(e)}), 502

if __name__ == "__main__":
    app.run(debug=True, port=8000)
