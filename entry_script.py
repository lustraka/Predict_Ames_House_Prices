import pickle
import os
import numpy as np
import pandas as pd

# from inference_schema.schema_decorators import input_schema, output_schema
# from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
# from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType

def init():
    #    global model
    model_path = os.path.join(os.environ['AZUREML_MODEL_DIR'], 'model.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

input_sample = pd.DataFrame(data=[{'MSSubClass': 0.0, 'MSZoning': 2.0, 'LotFrontage': 80.0, 'LotArea': 11622.0, 'Street': 1.0, 'Alley': 2.0, 'LotShape': 1.0, 'LandContour': 3.0, 'Utilities': 3.0, 'LotConfig': 4.0, 'LandSlope': 3.0, 'Neighborhood': 12.0, 'Condition1': 1.0, 'Condition2': 2.0, 'BldgType': 0.0, 'HouseStyle': 2.0, 'OverallQual': 6.0, 'OverallCond': 7.0, 'YearBuilt': 1961.0, 'YearRemodAdd': 1961.0, 'RoofStyle': 1.0, 'RoofMatl': 0.0, 'Exterior1st': 10.0, 'Exterior2nd': 13.0, 'MasVnrType': 2.0, 'MasVnrArea': 0.0, 'ExterQual': 3.0, 'ExterCond': 3.0, 'Foundation': 1.0, 'BsmtQual': 3.0, 'BsmtCond': 3.0, 'BsmtExposure': 1.0, 'BsmtFinType1': 3.0, 'BsmtFinSF1': 468.0, 'BsmtFinType2': 2.0, 'BsmtFinSF2': 144.0, 'BsmtUnfSF': 270.0, 'TotalBsmtSF': 882.0, 'Heating': 0.0, 'HeatingQC': 3.0, 'CentralAir': 2.0, 'Electrical': 5.0, '1stFlrSF': 896.0, '2ndFlrSF': 0.0, 'LowQualFinSF': 0.0, 'GrLivArea': 896.0, 'BsmtFullBath': 0.0, 'BsmtHalfBath': 0.0, 'FullBath': 1.0, 'HalfBath': 0.0, 'BedroomAbvGr': 2.0, 'KitchenAbvGr': 1.0, 'KitchenQual': 3.0, 'TotRmsAbvGrd': 5.0, 'Functional': 8.0, 'Fireplaces': 0.0, 'FireplaceQu': 0.0, 'GarageType': 1.0, 'GarageYrBlt': 1961.0, 'GarageFinish': 1.0, 'GarageCars': 1.0, 'GarageArea': 730.0, 'GarageQual': 3.0, 'GarageCond': 3.0, 'PavedDrive': 3.0, 'WoodDeckSF': 140.0, 'OpenPorchSF': 0.0, 'EnclosedPorch': 0.0, '3SsnPorch': 0.0, 'ScreenPorch': 120.0, 'PoolArea': 0.0, 'PoolQC': 0.0, 'Fence': 3.0, 'MiscFeature': 3.0, 'MiscVal': 0.0, 'MoSold': 6.0, 'YrSold': 2010.0, 'SaleType': 8.0, 'SaleCondition': 4.0}])

output_sample = np.array([0])

# @input_schema('data', PandasParameterType(input_sample))
# @output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        data = json.load(data)['data']
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
