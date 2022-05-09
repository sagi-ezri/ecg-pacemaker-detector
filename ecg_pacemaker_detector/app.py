import numpy as np
import wfdb
from flask import Flask, request, jsonify
import keras
import datetime
import json
import os

app = Flask(__name__)


# load model using keras
def load_model():
    global model
    model = keras.models.load_model("./model")


# welcome app
@app.route("/")
def home_endpoint():
    return "Welcome to the ECG Pacemaker Classifier - Sagi Ezri"


# predict app
@app.route("/predict", methods=["POST"])
def get_prediction():
    if request.method == "POST":
        age: int
        weight: float
        height: float
        nurse: int
        site: int
        device: str
        sex: int
        patient_id: str
        # get three files - metadata txt, signal data, signal header
        files = request.files.getlist("files")
        # get data posted as a json
        request_data = json.load(files[0])
        # get metadata
        if request_data:
            if "recording_date" in request_data:
                recording_date = datetime.datetime.strptime(
                    request_data["recording_date"], "%d/%m/%Y %H:%M:%S"
                )
            else:
                return "Error: please recording date"
            if "age" in request_data:
                age = int(request_data["age"])
            else:
                return "Error: please insert age"
            if "height" in request_data:
                height = float(request_data["height"])
            if "weight" in request_data:
                weight = float(request_data["weight"])
            if "nurse" in request_data:
                nurse = int(request_data["nurse"])
            if "site" in request_data:
                site = int(request_data["site"])
            if "device" in request_data:
                device = str(request_data["device"])
            if "sex" in request_data:
                sex = str(request_data["sex"])
            if "patient_id" in request_data:
                patient_id = str(request_data["patient_id"])
        # get the signal/header files
        request_file_data = files[1]
        request_file_header = files[2]
        # send the wfdb the filename without extension
        filename_without_ex = os.path.splitext(request_file_header.filename)[0]
        # save the uploaded files
        request_file_data.save(request_file_data.filename)
        request_file_header.save(request_file_header.filename)
        if request_file_data and request_file_header:
            # load the data into vector array
            raw_data = wfdb.rdsamp(filename_without_ex)
            ecg_signal_data = raw_data[0]
            # reshape to match the model dims
            ecg_signal_data = ecg_signal_data.reshape(
                1, ecg_signal_data.shape[0], ecg_signal_data.shape[1], 1
            )
        else:
            return "Error: please load a .dat and .hea files"
        if age > 18:
            # runs globally loaded model on the data
            prediction = model.predict(ecg_signal_data)
            pacemaker_bool_result = bool(np.argmax(prediction[0]))
            return "Pacemakr result: {}, Age: {}, Scan Date: {}".format(
                pacemaker_bool_result, age, recording_date
            )
        else:
            return "The patient is below 18 - Pacemakr result: {}, Age: {}, Scan Date: {}".format(
                None, age, recording_date
            )


def start() -> None:
    load_model()
    app.run(host="0.0.0.0", port=3000)
