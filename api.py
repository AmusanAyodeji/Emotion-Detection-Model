from flask import Flask, request, jsonify
from model import analyze_image_local
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok'})

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error':'no image provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error':'empty filename'}), 400
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    try:
        result = analyze_image_local(path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
