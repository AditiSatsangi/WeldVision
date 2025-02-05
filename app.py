from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import base64
from io import BytesIO
import os
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Path to your YOLO model
#model_path = 'D://A_Projects//Yolo_Deep_learning_modelsre//runs//detect//train2//weights//best.pt'
#model_path= 'D:\\A_Projects\\Yolo_Deep_learning_modelsre - Copy\\runs\\detect\\train2\\weights\\best.pt'

# Define the model file URL and local path
MODEL_URL = "https://aditistorageaccounts12.blob.core.windows.net/yolo/best.pt?sp=r&st=2025-02-05T18:31:11Z&se=2025-05-20T02:31:11Z&spr=https&sv=2022-11-02&sr=b&sig=5zc0bVw50UjaH3DQy3zaWVZDoIxXb3EzJs3ASqFgoBM%3D"
MODEL_PATH = "best.pt"

# Check if the model file exists; if not, download it
if not os.path.exists(MODEL_PATH):
    logging.info("Model file not found locally. Downloading from Azure Blob Storage...")
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()  # ✅ Raise an error for failed requests
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info("Model downloaded successfully.")
    except requests.RequestException as e:
        logging.error(f"Error downloading the model file: {e}")
        raise SystemExit("Failed to download the model. Exiting...")

# ✅ Load YOLO model using the correct path
try:
    model = YOLO(MODEL_PATH)
    categories = model.names  # Class names
except Exception as e:
    logging.error(f"Error loading YOLO model: {e}")
    raise SystemExit("Failed to load the YOLO model. Exiting...")
  

def process_and_predict_yolo(image_data):
    """
    Process the image and perform YOLO inference with optimizations.
    """
    try:
        # Decode base64 and convert to RGB image
        image = Image.open(BytesIO(base64.b64decode(image_data.split(",")[1]))).convert('RGB')

        # Resize image for faster inference (adjust size as needed)
        image_resized = image.resize((640, 640))
        image_data = np.array(image_resized)

        # Perform YOLOv8 inference
        results = model.predict(image_data, conf=0.25)  # Adjust confidence threshold

        # Annotate the image with predictions
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20) if os.path.exists("arial.ttf") else ImageFont.load_default()

        detected_objects = []
        for box in results[0].boxes:
            xyxy = box.xyxy.cpu().numpy()[0].tolist()
            confidence = float(box.conf.cpu().numpy()[0])
            cls = int(box.cls.cpu().numpy()[0])
            label = categories[cls]

            # Draw bounding box and label
            draw.rectangle(xyxy, outline="red", width=3)
            draw.text((xyxy[0], xyxy[1] - 10), f"{label} ({confidence:.2f})", fill="black", font=font)

            detected_objects.append({'label': label, 'confidence': confidence, 'box': xyxy})

        # Convert annotated image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return detected_objects, img_str

    except Exception as e:
        logging.error(f"Error in processing image: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_realtime', methods=['POST'])
def predict_realtime():
    try:
        data = request.get_json()
        image_data = data['image']

        # Perform object detection
        detected_objects, annotated_image = process_and_predict_yolo(image_data)

        return jsonify({'detected_objects': detected_objects, 'annotated_image': annotated_image})
    except Exception as e:
        logging.exception("Error in real-time prediction.")
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        if file:
            # Save the uploaded image temporarily
            image_path = "uploaded_image.jpg"
            file.save(image_path)

            # Open image and process
            image = Image.open(image_path)

            # Convert image to RGB if it's RGBA
            image = image.convert('RGB')
            image_data = np.array(image)

            # Perform inference with YOLOv8
            results = model(image_data)

            # Get the image for drawing bounding boxes
            draw = ImageDraw.Draw(image)

            # Use a font (optional: specify a font file path if you need custom fonts)
            try:
                font = ImageFont.truetype("arial.ttf", 20)  # Change font size here
            except IOError:
                font = ImageFont.load_default()

            # Parse the results and draw bounding boxes
            detected_objects = []
            for box in results[0].boxes:
                xyxy = box.xyxy.cpu().numpy()[0].tolist()  # Bounding box coordinates [xmin, ymin, xmax, ymax]
                confidence = float(box.conf.cpu().numpy()[0])  # Confidence score
                cls = int(box.cls.cpu().numpy()[0])  # Class ID
                label = categories[cls]  # Class label

                # Draw a red bounding box
                draw.rectangle(xyxy, outline="red", width=3)

                # Add label text above the box with black color
                text_position = (xyxy[0], xyxy[1] - 10)  # Position the label above the box
                text = f"{label} ({confidence:.2f})"
                draw.text(text_position, text, fill="black", font=font)

                detected_objects.append({
                    'label': label,
                    'confidence': confidence,
                    'box': xyxy
                })

            # Convert the annotated image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Return results in the result page
            return render_template('result.html', detected_objects=detected_objects, image_url=img_str)

    except Exception as e:
        logging.exception("Error occurred during prediction.")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
