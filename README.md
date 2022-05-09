# ECG Pacemaker Classifier
A pacemaker is a small device that's placed (implanted) in the chest to help control the heartbeat. It's used to prevent the heart from beating too slowly. Implanting a pacemaker in the chest requires a surgical procedure. The presence of a pacemaker on ECG is manifested by stimulation artifacts as demonstrated in the image below:
![image](https://user-images.githubusercontent.com/23264468/168440205-7ba62bea-3927-4422-9138-9d00274ec601.png)



## Description

In this mini-project, we created an algorithm to classify ECG records with a pacemaker and analyze its performance, and also deployment phase.

### Application:
* Implement a production level system that wraps your model. 
* Specifically, given an input signal and its metadata (e.g. age, sex, scan date, etc) the system checks if the patient is above 18 years old, 
if yes it applies the pacemaker algorithm and returns an output object containing the algorithm result (True/False),
patient age, and scan date; otherwise it throws an exception and returns the output object with patient age, scan date and empty algorithm result.

### NN Model:
![image](https://user-images.githubusercontent.com/23264468/168440174-edf9bc5c-aa50-4640-b283-10e97978b4b3.png)

* **Model explanation**:

  * I've created a convolution neural network based model with 2 convolution layers and 2 maxpooling layers.
  * Applied flat layer to get all features into one dimension. 
  * Applied one dense layer.
  * To fine tune the model and finally output layer with 2 neurons (True, False) is being added.
  * Throughout the model, I have used relu activation.
## Getting Started

### Prerequisites

* WSL 2 platform to run dockerize environment Or cloud platform with linux OS and docker package
* The application is fully containerized for production
* The docker container could be also as development environment for further application uses 

### Installing

* run:
```
docker pull sagiezri/ecg_pacemaker_classifier:version1.0
```

### Executing program

* Server side—run:
```
sudo docker run -p 80:3000 sagiezri/ecg_pacemaker_classifier:version1.0
```
* To run POST client request run from your machine:
```
curl -F files=@ecg_predict.txt -F files=@00001_lr.dat -F files=@00001_lr.hea http://server-public-dns/predict
```
* An example for the ecg_predict.txt file (we convert the txt file to JSON):
```
{
    "recording_date":"01/11/1984  8:27:32",
    "age":18,
    "height":55,
    "weight": 80,
    "nurse": 0,
    "site": 2,
    "device": "CS-12   E",
    "sex": "Male",
    "patient_id": 1
}
```
* The signal data and header files should be also attach as mentioned above in the same order


## Help

Any advice for common problems or issues, ping me.

## Authors

* Sagi Ezri <sagi.ezri@gmail.com>

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details





