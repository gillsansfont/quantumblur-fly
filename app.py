from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io, base64
import quantumblur

app = Flask(__name__)
CORS(app)

@app.route('/quantumblur', methods=['POST'])
def blur_frame():
    header, data = request.json['image'].split(',', 1)
    img = Image.open(io.BytesIO(base64.b64decode(data)))
    out = quantumblur.quantum_blur(img)
    buf = io.BytesIO()
    out.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return jsonify({ 'image': f'data:image/png;base64,{b64}' })

if __name__ == '__main__':
    app.run(port=5000)
