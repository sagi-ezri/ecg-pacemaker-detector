
# ECG Pacemaker Classifier

A pacemaker is a small device implanted in the chest to help regulate the heartbeat, typically used to prevent the heart from beating too slowly. The presence of a pacemaker on an ECG is indicated by stimulation artifacts, as shown in the image below:

![Pacemaker ECG](https://user-images.githubusercontent.com/23264468/168440205-7ba62bea-3927-4422-9138-9d00274ec601.png)

## Project Overview

This project involves the development of an algorithm to classify ECG records for the presence of a pacemaker. The solution includes both model development and deployment phases, designed to operate in a production environment.

### Key Features

- **Production-Ready Application**: A fully containerized system that wraps the pacemaker classification model, ensuring ease of deployment and scalability.
- **Intelligent Processing**: The application processes input ECG signals and metadata (e.g., age, sex, scan date). If the patient is over 18 years old, the algorithm runs and returns the classification result along with the patient's age and scan date. For patients under 18, the algorithm skips processing, returning an empty result.

## Neural Network Model

![Neural Network Model](https://user-images.githubusercontent.com/23264468/168440174-edf9bc5c-aa50-4640-b283-10e97978b4b3.png)

### Model Architecture

- **Convolutional Layers**: The model is built using a Convolutional Neural Network (CNN) with two convolutional layers and two max-pooling layers.
- **Flattening**: A flattening layer is used to convert the features into a single dimension.
- **Dense Layer**: A dense layer processes the flattened features.
- **Output Layer**: The final output layer consists of two neurons (True/False) to predict the presence of a pacemaker.
- **Activation Function**: ReLU activation is used throughout the model.

## Getting Started

### Prerequisites

- **Platform**: This application runs on a WSL 2 platform or any Linux-based cloud environment with Docker installed.
- **Containerization**: The application is fully containerized, supporting both production and development environments.

### Installation

To set up the application, pull the Docker image using the following command:

```bash
docker pull sagiezri/ecg_pacemaker_classifier:version1.0
```

### Running the Application

#### Server Side

To run the server, execute:

```bash
sudo docker run -p 80:3000 sagiezri/ecg_pacemaker_classifier:version1.0
```

#### Client Side

To make a POST request to the server, use the following `curl` command:

```bash
curl -F files=@ecg_predict.txt -F files=@00001_lr.dat -F files=@00001_lr.hea http://server-public-dns/predict
```

#### Example Input File

Here’s an example of the `ecg_predict.txt` file, which should be converted to JSON:

```json
{
    "recording_date": "01/11/1984 08:27:32",
    "age": 18,
    "height": 55,
    "weight": 80,
    "nurse": 0,
    "site": 2,
    "device": "CS-12 E",
    "sex": "Male",
    "patient_id": 1
}
```

The signal data and header files should be attached in the same order as mentioned above.

## Troubleshooting

For common issues or questions, feel free to reach out to me.

## Author

- **Sagi Ezri** - [Email](mailto:sagi.ezri@gmail.com)

## Version History

- **0.1**
  - Initial Release

## License

This project is licensed under the [Your License Name Here] License - see the LICENSE.md file for details.