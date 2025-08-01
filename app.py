# at top of app.py
from flask import Flask, request, jsonify
from flask_cors import CORS       # ← add this
from PIL import Image
import io, base64
from quantumblur import QuantumBlur

app = Flask(__name__)
CORS(app)                         # ← and this

blur_engine = QuantumBlur()

@app.route('/quantumblur', methods=['POST'])
def quantum_blur():
    file = request.files['image']
    image = Image.open(file.stream)
    blurred = blur_engine(image)
    buffer = io.BytesIO()
    blurred.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return jsonify({'image': f'data:image/png;base64,{img_str}'})
