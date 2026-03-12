import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the model (ensure vgg19.h5 is in the same folder)
MODEL_PATH = 'vgg19.h5'
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    f = request.files['file']
    if f.filename == '':
        return "No selected file"
    
    basepath = os.path.dirname(__file__)
    upload_path = os.path.join(basepath, 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    file_path = os.path.join(upload_path, secure_filename(f.filename))
    f.save(file_path)

    preds = model_predict(file_path, model)
    # Decode: [[('id', 'label', prob), ...]]
    decoded = decode_predictions(preds, top=1)
    result = str(decoded[0][0][1]).replace('_', ' ')
    return result

if __name__ == '__main__':
    app.run(debug=True)