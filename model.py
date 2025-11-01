from deepface import DeepFace
import cv2
import os

def analyze_image_local(image_path):
    result = DeepFace.analyze(img_path = image_path, actions = ['emotion'], enforce_detection=False)
    out = {}
    if isinstance(result, list):
        result = result[0]
    out['dominant_emotion'] = result.get('dominant_emotion')
    out['emotion'] = result.get('emotion')
    out['region'] = result.get('region')
    return out