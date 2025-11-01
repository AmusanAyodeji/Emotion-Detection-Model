from flask import Flask, request, jsonify
from model import analyze_image_local
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "no image provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400

    filename = secure_filename(file.filename)
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(img_path)

    if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
        return jsonify({"error": "file not saved properly"}), 400

    img = cv2.imread(img_path)
    if img is None:
        return jsonify({"error": "invalid or unreadable image"}), 400

    try:
        result = analyze_image_local(img)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
