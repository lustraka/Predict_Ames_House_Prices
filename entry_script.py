import pickle
import os
import numpy as np
import pandas as pd
import json

def init():
    global model
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], 'model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

def run(data):
    try:
        data = json.loads(data)['data']
        data = pd.DataFrame.from_dict(data)
        print(f'data.shape = {data.shape}')
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
