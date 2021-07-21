# Import dependencies
! pip install py7zr --quiet
! pip install kaggle --upgrade --quiet

import os
import py7zr
import pandas as pd

# Set the enviroment variables
os.environ['KAGGLE_USERNAME'] = "lubomrstraka"
os.environ['KAGGLE_KEY'] = "c7347462ef834e6645ce238c2f2fa561"

# Download and unpack data
! kaggle competitions download -c mercari-price-suggestion-challenge

for file in ['train.tsv.7z']: # also 'test.tsv.7z' if relevant
  with py7zr.SevenZipFile(file, 'r') as archive:
    archive.extract()

# Read data to pd.DataFrame
train = pd.read_csv('train.tsv', sep='\t')

# Transform data using pandas

# Store preprocessed data locally
os.makedirs('./data', exist_ok=True)
with open('./data/train.csv', 'w') as writer:
    train.to_csv(writer, index=False)

# ----------------------------------------------

# Import dependencies
from azureml.core import Workspace
from azureml.data.dataset_factory import TabularDatasetFactory
import pandas as pd

# Get workspace
ws = Workspace.from_config()

print('Workspace name: ' + ws.name, 
      'Azure region: ' + ws.location, 
      'Subscription id: ' + ws.subscription_id, 
      'Resource group: ' + ws.resource_group, sep = '\n')

# Upload data to AzureBlobDatastore
blob = ws.get_default_datastore()
blob.upload(src_dir='data', target_path='data', overwrite=True)

# Create the final dataset for experiments
training_data = TabularDatasetFactory.from_delimited_files(blob.path('data/train.csv'))

# Register the dataset
dataset_name = 'mercari-train-data'
ds = training_data.register(workspace=ws, name=dataset_name, description='Mercari training data after preprocessing.')

# ----------------------------------------------

dataset_name = 'mercari-train-data'

# Get a dataset by name
train_ds = Dataset.get_by_name(workspace=ws, name=dataset_name)

train = train_ds.to_pandas_dataframe()
train.info()
