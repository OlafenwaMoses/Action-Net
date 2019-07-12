from io import open
import requests
import shutil
from zipfile import ZipFile
from imageai.Prediction.Custom import ModelTraining, CustomImagePrediction
import os

execution_path = os.getcwd()

SOURCE_PATH = "https://github.com/OlafenwaMoses/Action-Net/releases/download/v1/action_net_v1.zip"
FILE_DIR = os.path.join(execution_path, "action_net_v1.zip")
DATASET_DIR = os.path.join(execution_path, "action_net_v1.zip")


def download_action_net():
    if (os.path.exists(FILE_DIR) == False):
        print("Downloading action_net_v1.zip")
        data = requests.get(SOURCE_PATH,
                            stream=True)

        with open(FILE_DIR, "wb") as file:
            shutil.copyfileobj(data.raw, file)
        del data

        extract = ZipFile(FILE_DIR)
        extract.extractall(execution_path)
        extract.close()


def train_action_net():
    download_action_net()

    trainer = ModelTraining()
    trainer.setModelTypeAsResNet()
    trainer.setDataDirectory("action_net_v1")
    trainer.trainModel(num_objects=16, num_experiments=200, batch_size=32, save_full_model=True,
                       enhance_data=True)

def run_predict():
    predictor = CustomImagePrediction()
    predictor.setModelPath(model_path="action_net_ex-060_acc-0.745313.h5")
    predictor.setJsonPath(model_json="model_class.json")
    predictor.loadFullModel(num_objects=16)

    predictions, probabilities = predictor.predictImage(image_input="images/5.jpg", result_count=4)
    for prediction, probability in zip(predictions, probabilities):
        print(prediction, " : ", probability)

#Un-comment the line below to train your model
#train_action_net()

#Un-comment the line below to run predictions
run_predict()