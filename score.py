from azureml.core import Workspace
from azureml.core.model import Model

def init():
    ws = Workspace.from_config()
    model = Model(ws, 'Ames-Housing-XGB-Model')


def run(data):
    return model.predict(data)
