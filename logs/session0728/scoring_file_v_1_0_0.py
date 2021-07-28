# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
import joblib

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


input_sample = pd.DataFrame({"1stFlrSF": pd.Series([0], dtype="int64"), "2ndFlrSF": pd.Series([0], dtype="int64"), "3SsnPorch": pd.Series([0], dtype="int64"), "Alley": pd.Series([0], dtype="int64"), "BedroomAbvGr": pd.Series([0], dtype="int64"), "BldgType": pd.Series([0], dtype="int64"), "BsmtCond": pd.Series([0], dtype="int64"), "BsmtExposure": pd.Series([0], dtype="int64"), "BsmtFinSF1": pd.Series([0.0], dtype="float64"), "BsmtFinSF2": pd.Series([0.0], dtype="float64"), "BsmtFinType1": pd.Series([0], dtype="int64"), "BsmtFinType2": pd.Series([0], dtype="int64"), "BsmtFullBath": pd.Series([0.0], dtype="float64"), "BsmtHalfBath": pd.Series([0.0], dtype="float64"), "BsmtQual": pd.Series([0], dtype="int64"), "BsmtUnfSF": pd.Series([0.0], dtype="float64"), "CentralAir": pd.Series([0], dtype="int64"), "Condition1": pd.Series([0], dtype="int64"), "Condition2": pd.Series([0], dtype="int64"), "Electrical": pd.Series([0], dtype="int64"), "EnclosedPorch": pd.Series([0], dtype="int64"), "ExterCond": pd.Series([0], dtype="int64"), "ExterQual": pd.Series([0], dtype="int64"), "Exterior1st": pd.Series([0], dtype="int64"), "Exterior2nd": pd.Series([0], dtype="int64"), "Fence": pd.Series([0], dtype="int64"), "FireplaceQu": pd.Series([0], dtype="int64"), "Fireplaces": pd.Series([0], dtype="int64"), "Foundation": pd.Series([0], dtype="int64"), "FullBath": pd.Series([0], dtype="int64"), "Functional": pd.Series([0], dtype="int64"), "GarageArea": pd.Series([0.0], dtype="float64"), "GarageCars": pd.Series([0.0], dtype="float64"), "GarageCond": pd.Series([0], dtype="int64"), "GarageFinish": pd.Series([0], dtype="int64"), "GarageQual": pd.Series([0], dtype="int64"), "GarageType": pd.Series([0], dtype="int64"), "GarageYrBlt": pd.Series([0.0], dtype="float64"), "GrLivArea": pd.Series([0], dtype="int64"), "HalfBath": pd.Series([0], dtype="int64"), "Heating": pd.Series([0], dtype="int64"), "HeatingQC": pd.Series([0], dtype="int64"), "HouseStyle": pd.Series([0], dtype="int64"), "KitchenAbvGr": pd.Series([0], dtype="int64"), "KitchenQual": pd.Series([0], dtype="int64"), "LandContour": pd.Series([0], dtype="int64"), "LandSlope": pd.Series([0], dtype="int64"), "LotArea": pd.Series([0], dtype="int64"), "LotConfig": pd.Series([0], dtype="int64"), "LotFrontage": pd.Series([0.0], dtype="float64"), "LotShape": pd.Series([0], dtype="int64"), "LowQualFinSF": pd.Series([0], dtype="int64"), "MSSubClass": pd.Series([0], dtype="int64"), "MSZoning": pd.Series([0], dtype="int64"), "MasVnrArea": pd.Series([0.0], dtype="float64"), "MasVnrType": pd.Series([0], dtype="int64"), "MiscFeature": pd.Series([0], dtype="int64"), "Neighborhood": pd.Series([0], dtype="int64"), "OpenPorchSF": pd.Series([0], dtype="int64"), "OverallCond": pd.Series([0], dtype="int64"), "OverallQual": pd.Series([0], dtype="int64"), "PavedDrive": pd.Series([0], dtype="int64"), "PoolArea": pd.Series([0], dtype="int64"), "RoofMatl": pd.Series([0], dtype="int64"), "RoofStyle": pd.Series([0], dtype="int64"), "SaleCondition": pd.Series([0], dtype="int64"), "SaleType": pd.Series([0], dtype="int64"), "ScreenPorch": pd.Series([0], dtype="int64"), "Street": pd.Series([0], dtype="int64"), "TotRmsAbvGrd": pd.Series([0], dtype="int64"), "TotalBsmtSF": pd.Series([0.0], dtype="float64"), "Utilities": pd.Series([0], dtype="int64"), "WoodDeckSF": pd.Series([0], dtype="int64"), "YearBuilt": pd.Series([0], dtype="int64"), "YearRemodAdd": pd.Series([0], dtype="int64"), "YrSold": pd.Series([0], dtype="int64"), "MedNhbdArea": pd.Series([0.0], dtype="float64")})
output_sample = np.array([0])
try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script')
except:
    pass


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    path = os.path.normpath(model_path)
    path_split = path.split(os.sep)
    log_server.update_custom_dimensions({'model_name': path_split[-3], 'model_version': path_split[-2]})
    try:
        logger.info("Loading model from path.")
        model = joblib.load(model_path)
        logger.info("Loading successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
