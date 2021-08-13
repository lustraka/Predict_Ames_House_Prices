"""Train, evaluate and log metrics for selected ML algorithm 
in the Azure workspace context."""

import argparse
import os
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype # ordered categorical data type, see encode()
import pickle

from azureml.core.run import Run
from azureml.core import Workspace

from xgboost import XGBRegressor 
# (1) "AssertError:read can not have position excceed buffer length" when loading saved model
# (2) "ResolvePackageNotFound: - xgboost[version='<=0.90']" when building an image to prevent (1)
# from azureml.automl.runtime.shared.model_wrappers import XGBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def load_data_raw(source='local'):
    """Load train and test data from Kaggle.com."""
    import os

    if source == 'kaggle':
        # Download the Ames Housing Dataset
        # Set the enviroment variables
        import zipfile
        os.environ['KAGGLE_USERNAME'] = "lubomrstraka"
        os.environ['KAGGLE_KEY'] = "c7347462ef834e6645ce238c2f2fa561"
        
        # Import dependencies
        os.system("pip install kaggle --upgrade --quiet")

        # Download datasets
        os.system("kaggle competitions download -c house-prices-advanced-regression-techniques --quiet")
        
        # Extract data
        with zipfile.ZipFile('house-prices-advanced-regression-techniques.zip', 'r') as archive:
            archive.extractall()

        # Read Train & Test Baseline Data
        train_bl = pd.read_csv('train.csv', index_col='Id')
        test_bl = pd.read_csv('test.csv', index_col='Id')
    
    # Using local data prevents "Too many requests" response from Kaggle
    elif source == 'local': 
        train_bl = pd.read_csv('data/train.csv', index_col='Id')
        test_bl = pd.read_csv('data/test.csv', index_col='Id')
    
    else:
        print('Missing data!')
        train_bl = pd.DataFrame()
        test_bl = pd.DataFrame()


    return train_bl, test_bl

# The numeric features are already encoded correctly (`float` for
# continuous, `int` for discrete), but the categoricals we'll need to
# do ourselves. Note in particular, that the `MSSubClass` feature is
# read as an `int` type, but is actually a (nominative) categorical.

# The categorical features nominative (unordered)
catn = ["MSSubClass", "MSZoning", "Street", "Alley", "LandContour", "LotConfig",
        "Neighborhood", "Condition1", "Condition2", "BldgType", "HouseStyle", 
        "RoofStyle", "RoofMatl", "Exterior1st", "Exterior2nd", "MasVnrType", 
        "Foundation", "Heating", "CentralAir", "GarageType", "MiscFeature", 
        "SaleType", "SaleCondition"]


# The categorical features ordinal (ordered) 

# Pandas calls the categories "levels"
five_levels = ["Po", "Fa", "TA", "Gd", "Ex"]
ten_levels = list(range(10))

cato = {
    "OverallQual": ten_levels,
    "OverallCond": ten_levels,
    "ExterQual": five_levels,
    "ExterCond": five_levels,
    "BsmtQual": five_levels,
    "BsmtCond": five_levels,
    "HeatingQC": five_levels,
    "KitchenQual": five_levels,
    "FireplaceQu": five_levels,
    "GarageQual": five_levels,
    "GarageCond": five_levels,
    "PoolQC": five_levels,
    "LotShape": ["Reg", "IR1", "IR2", "IR3"],
    "LandSlope": ["Sev", "Mod", "Gtl"],
    "BsmtExposure": ["No", "Mn", "Av", "Gd"],
    "BsmtFinType1": ["Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    "BsmtFinType2": ["Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    "Functional": ["Sal", "Sev", "Maj1", "Maj2", "Mod", "Min2", "Min1", "Typ"],
    "GarageFinish": ["Unf", "RFn", "Fin"],
    "PavedDrive": ["N", "P", "Y"],
    "Utilities": ["NoSeWa", "NoSewr", "AllPub"],
    "CentralAir": ["N", "Y"],
    "Electrical": ["Mix", "FuseP", "FuseF", "FuseA", "SBrkr"],
    "Fence": ["MnWw", "GdWo", "MnPrv", "GdPrv"],
}

# Add a None level for missing values
cato = {key: ["None"] + value for key, value in
                  cato.items()}


def encode_dtypes(df):
    """Encode nominal and ordinal categorical variables."""

    global catn, cato

    # Nominal categories
    for name in catn:
        df[name] = df[name].astype("category")
        # Add a None category for missing values
        if "None" not in df[name].cat.categories:
            df[name].cat.add_categories("None", inplace=True)
    # Ordinal categories
    for name, levels in cato.items():
        df[name] = df[name].astype(CategoricalDtype(levels,
                                                    ordered=True))
    return df

def impute_missing(df):
    """Impute zeros to numerical and None to categorical variables."""

    for name in df.select_dtypes("number"):
        df[name] = df[name].fillna(0)
    for name in df.select_dtypes("category"):
        df[name] = df[name].fillna("None")
    return df

def clean_data(df):
    """Remedy typos and mistakes based on EDA."""

    global cato
    # YearRemodAdd: Remodel date (same as construction date if no remodeling or additions)
    df.YearRemodAdd = np.where(df.YearRemodAdd < df.YearBuilt, df.YearBuilt, df.YearRemodAdd)
    assert len(df.loc[df.YearRemodAdd < df.YearBuilt]) == 0, 'Check YearRemodAdd - should be greater or equal then YearBuilt'
    
    # Check range of years
    yr_max = 2022
    # Some values of GarageYrBlt are corrupt. Fix them by replacing them with the YearBuilt
    df.GarageYrBlt = np.where(df.GarageYrBlt > yr_max, df.YearBuilt, df.GarageYrBlt)
    assert df.YearBuilt.max() < yr_max and df.YearBuilt.min() > 1800, 'Check YearBuilt min() and max()'
    assert df.YearRemodAdd.max() < yr_max and df.YearRemodAdd.min() > 1900, 'Check YearRemodAdd min() and max()'
    assert df.YrSold.max() < yr_max and df.YrSold.min() > 2000, 'Check YrSold min() and max()'
    assert df.GarageYrBlt.max() < yr_max and df.GarageYrBlt.min() >= 0, 'Check GarageYrBlt min() and max()'
    
    # Check values of ordinal catagorical variables
    for k in cato.keys():
      assert set(df[k].unique()).difference(df[k].cat.categories) == set(), f'Check values of {k}'
    
    # Check typos in nominal categorical variables
    df['Exterior2nd'] = df['Exterior2nd'].replace({'Brk Cmn':'BrkComm', 'CmentBd':'CemntBd', 'Wd Shng':'WdShing'})
    # Renew a data type after replacement
    df['Exterior2nd'] = df['Exterior2nd'].astype("category")
    if "None" not in df['Exterior2nd'].cat.categories:
        df['Exterior2nd'].cat.add_categories("None", inplace=True)

    return df

def label_encode(df):
    """Encode categorical variables using their dtype setting."""

    X = df.copy()
    for colname in X.select_dtypes(["category"]):
        X[colname] = X[colname].cat.codes
    return X

def load_data_clean():
    """Load and data and pre-process them."""

    train_bl, test_bl = load_data_raw()

    train = train_bl.copy()
    train = encode_dtypes(train)
    train = impute_missing(train)
    train = clean_data(train)

    test = test_bl.copy()
    test = encode_dtypes(test)
    test = impute_missing(test)
    test = clean_data(test)

    return train, test

def main():
    train, _ = load_data_clean()

    X_train, X_test = train_test_split(label_encode(train))
    y_train = X_train.pop('SalePrice')
    y_test = X_test.pop('SalePrice')

    print(f"X_train.shape = {X_train.shape}, X_test.shape = {X_test.shape}")

    run = Run.get_context()

    parser = argparse.ArgumentParser()

    parser.add_argument('--learning_rate', type=float, default=0.1,
                    help='Step size shrinkage used in update to prevent overfiffing')

    parser.add_argument('--gamma', type=float, default=2,
                    help='Minimum loss reduction required to make a further partition on a leaf node of the tree')

    parser.add_argument('--max_depth', type=int, default=3,
                    help='Maximum depth of a tree')

    args = parser.parse_args()
    run.log('Learning rate', np.float(args.learning_rate))
    run.log('Gamma', np.float(args.gamma))
    run.log('Maximum depth', np.float(args.max_depth))

    model = XGBRegressor(learning_rate=args.learning_rate, gamma=args.gamma, max_depth=args.max_depth, objective='reg:squarederror')
    # model = XGBoostRegressor(learning_rate=args.learning_rate, gamma=args.gamma, max_depth=args.max_depth, objective='reg:squarederror')
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    run.log("r2_score", np.float(r2))
    print(f'Writting r2 score = {r2} into a log.')

    os.makedirs('./outputs', exist_ok=True)
    with open('outputs/model.pkl', 'wb') as file:
        pickle.dump(model, file)

if __name__ == '__main__':
    main()