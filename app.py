import streamlit as st
import requests
from PIL import Image
import io

BACKEND_URL = "https://emotion-detection-api-ra6n.onrender.com/analyze"

st.set_page_config(page_title='Emotion Detector', layout='centered')
st.title('😊 Emotion Detection App')
st.write('Upload a picture or use your camera to detect emotions in real time.')

mode = st.radio("Choose input mode:", ["Upload Image", "Use Camera"])

def send_to_backend(pil_image):
    """Send a PIL image to Flask backend and return response JSON."""
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    response = requests.post(
        BACKEND_URL,
        files={'image': ('input.jpg', img_bytes, 'image/jpeg')}
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Backend returned error: {response.text}")
        return None

if mode == "Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded image", use_column_width=True)

        if st.button("Analyze Emotion"):
            with st.spinner("Analyzing..."):
                try:
                    result = send_to_backend(image)
                    if result:
                        st.success("Analysis complete!")
                        st.write("Dominant Emotion:", result.get("dominant_emotion"))
                        if 'emotion' in result:
                            st.table(result["emotion"])
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Is Flask running?")

elif mode == "Use Camera":
    camera_image = st.camera_input("Take a photo")
    if camera_image:
        image = Image.open(camera_image).convert("RGB")
        st.image(image, caption="Captured photo", use_column_width=True)

        if st.button("Analyze Emotion"):
            with st.spinner("Analyzing..."):
                try:
                    result = send_to_backend(image)
                    if result:
                        st.success("Analysis complete!")
                        st.write("Dominant Emotion:", result.get("dominant_emotion"))
                        if 'emotion' in result:
                            st.table(result["emotion"])
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Is Flask running?")
