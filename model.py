from deepface import DeepFace
import numpy as np

def analyze_image_local(img):
    result = DeepFace.analyze(
        img_path=img,           
        actions=["emotion"],
        enforce_detection=False
    )
    if isinstance(result, list):
        result = result[0]

    return {
        "dominant_emotion": result.get("dominant_emotion"),
        "emotion": result.get("emotion"),
        "region": result.get("region")
    }
