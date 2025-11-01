from deepface import DeepFace
import numpy as np

def convert_to_native(obj):
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(v) for v in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    else:
        return obj
    

def analyze_image_local(img):
    result = DeepFace.analyze(
        img_path=img,
        actions=["emotion"],
        enforce_detection=False
    )
    if isinstance(result, list):
        result = result[0]

    from model import convert_to_native
    result = convert_to_native(result)

    return {
        "dominant_emotion": result.get("dominant_emotion"),
        "emotion": result.get("emotion"),
        "region": result.get("region")
    }

