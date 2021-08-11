import joblib
import os

def init():
    global model
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], 'model.joblib')
    model = joblib.load(model_path)


def run(data):
    return model.predict(data)
