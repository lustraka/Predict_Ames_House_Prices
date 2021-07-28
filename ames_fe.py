"""Feature engineering module for Ames Housing Dataset."""

import pandas as pd
import ames

def drop_uninformative(df):
    """Drops columns with MI Score equal to 0."""
    cols_uninformative = ['PoolQC', 'MiscVal', 'MoSold']
    df = df.drop(columns=cols_uninformative)
    return df

def mathematical_transforms(df):
    """Get a couple of feature based on mathematical formulas."""
    X = pd.DataFrame()
    X["Spaciousness"] = (df['1stFlrSF'] + df['2ndFlrSF']) / df.TotRmsAbvGrd
    X["TotalOutsideSF"] = df.WoodDeckSF + df.OpenPorchSF + df.EnclosedPorch + df['3SsnPorch'] + df.ScreenPorch
    X['OverallQC'] = df.OverallQual.cat.codes * df.OverallCond.cat.codes
    X['BsmtQSF'] = df.BsmtQual.cat.codes * df.TotalBsmtSF
    return X

def interactions(df):
    """Get one-hot encoding of garage types * garage area."""
    X = pd.get_dummies(df.GarageType, prefix="Garage")
    X = X.mul(df.GarageArea, axis=0)
    return X

def counts(df):
    """Count number of porch types."""
    X = pd.DataFrame()
    X["PorchTypes"] = df[[
        "WoodDeckSF",
        "OpenPorchSF",
        "EnclosedPorch",
        "3SsnPorch",
        "ScreenPorch",
    ]].gt(0.0).sum(axis=1)
    return X

def group_transforms(df):
    """Group Neighborhood by median of GrLivArea."""
    X = pd.DataFrame()
    X["MedNhbdArea"] = df.groupby("Neighborhood")["GrLivArea"].transform("median")
    return X

def pca_inspired(df):
    """Create features inspired by Principal Component Analysis."""
    X = pd.DataFrame()
    X['AreaGRBsmt'] = df.GrLivArea + df.TotalBsmtSF
    return X

def tailor_ames(train, test=None):
    """Add features based on Exploratory Data Analysis of Ames Housing dataset."""

    df = train.copy()
    # The test set should be transformed in the same way as the train set.
    if test is not None:
      dft = test.copy()
      df = pd.concat([df, dft], sort=False)
      df = ames.encode_dtypes(df) # Restore dtypes encoding

    df = drop_uninformative(df)
    
    # Transformations
    #df = df.join(mathematical_transforms(df))
    #df = df.join(interactions(df))
    #df = df.join(counts(df))
    df = df.join(group_transforms(df))

    # PCA inspired
    #df = df.join(pca_inspired(df))

    df = ames.label_encode(df)

    # Reform splits
    if test is not None:
      dft = df.loc[test.index, :]
      dft.drop(columns=['SalePrice'], inplace=True)
      df.drop(test.index, inplace=True)

    if test is not None:
      return df, dft
    else:
      return df

def load_data_tailored():
    """Load data with adjusted features."""
    train, test = tailor_ames(*ames.load_data_clean())
    return train, test
