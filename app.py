from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io, base64

import quantumblur                     # our blur library
from qiskit import Aer, IBMQ           # Qiskit backends

app = Flask(__name__)
CORS(app)

# 1) try real hardware; otherwise use Aer simulator
try:
    IBMQ.load_account()               # you must have set your IBMQ token locally
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = provider.get_backend('ibmq_qasm_simulator')
except Exception:
    backend = Aer.get_backend('aer_simulator')

@app.route('/quantumblur', methods=['POST'])
def blur_frame():
    # decode incoming PNG
    data_url = request.json['image']
    header, encoded = data_url.split(',', 1)
    img = Image.open(io.BytesIO(base64.b64decode(encoded)))

    # 2) run the blur with our chosen backend
    #    you can also tweak shots, seed, etc. here!
    blurred_img = quantumblur.quantum_blur(
        img,
        backend=backend,
        shots=2048
    )

    # 3) encode back to base64
    buf = io.BytesIO()
    blurred_img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return jsonify({'image': f'data:image/png;base64,{b64}'})

if __name__ == '__main__':
    app.run(port=5000)
