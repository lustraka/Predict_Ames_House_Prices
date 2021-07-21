from azureml.core import Workspace, Dataset

ws = Workspace.from_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep='\n')

dataset = Dataset.get_by_name(ws, name='mercari-train-data')
print(dataset.to_pandas_dataframe().info())