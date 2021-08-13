import pickle
import os

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType

def init():
    global model
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], 'model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(model_path)


def run(data):
    return model.predict(data)
