import os
import json
import datetime
import numpy as np
import wfdb
from flask import Flask, request, jsonify
from keras.models import load_model

app = Flask(__name__)

model = load_model('./model/best')

@app.route('/')
def home_endpoint():
    """Welcome endpoint"""
    return 'Welcome to the ECG Pacemaker Classifier - Sagi Ezri'


@app.route('/predict', methods=['POST'])
def get_prediction():
    """Receive files and predict pacemaker"""
    try:
        metadata = request.json
        if not metadata:
            return jsonify({'error': 'No JSON metadata provided'}), 400

        required_fields = ['age', 'recording_date']
        missing_fields = [field for field in required_fields if field not in metadata]
        if missing_fields:
            return jsonify({'error': f'Missing fields in metadata: {", ".join(missing_fields)}'}), 400

        age = int(metadata['age'])
        recording_date = datetime.datetime.strptime(metadata['recording_date'], '%d/%m/%Y %H:%M:%S')

        height = float(metadata.get('height', 0))
        weight = float(metadata.get('weight', 0))
        nurse = int(metadata.get('nurse', 0))
        site = int(metadata.get('site', 0))
        device = str(metadata.get('device', 'unknown'))
        sex = str(metadata.get('sex', 'unknown'))
        patient_id = str(metadata.get('patient_id', 'unknown'))

        files = request.files.getlist('files')
        if len(files) < 2:
            return jsonify({'error': 'Insufficient files uploaded'}), 400

        signal = files[1].filename
        header = files[2].filename

        filename_without_ex = os.path.splitext(header)[0]
        data, _ = wfdb.rdsamp(filename_without_ex)
        ecg_signal_data = data.reshape((1,) + data.shape + (1,))

        prediction = model.predict(ecg_signal_data)
        pacemaker_result = bool(np.argmax(prediction[0]))

        output = {
            'pacemaker_result': pacemaker_result if age > 18 else None,
            'age': age,
            'recording_date': str(recording_date)
        }

        return jsonify(output)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
