import numpy as np
import wfdb
from flask import Flask, request
import keras
import datetime
import json
import os

app = Flask(__name__)

# Load model using keras
model = keras.models.load_model('./model/best')


@app.route('/')
def home_endpoint():
    """Welcome app"""
    return 'Welcome to the ECG Pacemaker Classifier - Sagi Ezri'


@app.route('/predict', methods=['POST'])
def get_prediction():
    """Receive files and predict pacemaker"""
    # Get data
    age = request.json.get('age')
    weight = request.json.get('weight')
    height = request.json.get('height')
    nurse = request.json.get('nurse')
    site = request.json.get('site')
    device = request.json.get('device')
    sex = request.json.get('sex')
    patient_id = request.json.get('patient_id')

    # Get files
    files = request.files.getlist('files')
    metadata = json.load(files[0])
    signal = files[1].filename
    header = files[2].filename

    # Parse metadata
    if 'recording_date' in metadata:
        recording_date = datetime.datetime.strptime(metadata['recording_date'],
                                                     '%d/%m/%Y %H:%M:%S')
    else:
        return {'error': 'Please provide recording date'}
    if 'age' not in metadata:
        return {'error': 'Please provide age'}
    if 'height' in metadata:
        height = float(height)
    if 'weight' in metadata:
        weight = float(weight)
    if 'nurse' in metadata:
        nurse = int(nurse)
    if 'site' in metadata:
        site = int(site)
    if 'device' in metadata:
        device = str(device)
    if 'sex' in metadata:
        sex = str(sex)
    if 'patient_id' in metadata:
        patient_id = str(patient_id)

    # Load data into vector array
    filename_without_ex = os.path.splitext(header)[0]
    data, _ = wfdb.rdsamp(filename_without_ex)
    ecg_signal_data = data.reshape((1,) + data.shape + (1,))

    # Run model
    prediction = model.predict(ecg_signal_data)
    pacemaker_result = bool(np.argmax(prediction[0]))

    # Format output
    if age > 18:
        output = {'pacemaker_result': pacemaker_result,
                  'age': age,
                  'recording_date': str(recording_date)}
    else:
        output = {'pacemaker_result': None,
                  'age': age,
                  'recording_date': str(recording_date)}
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
