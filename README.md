# Predict House Prices in Ames, Iowa

(🚧 under construction 🚧)

This is a final project of the Udacity Machine Learning Engineer with Microsoft Azure Nanodegree Program. The project's goal is to train and deploy a machine learning model for **prediction of the sales price based on parameters of a house**. The project starts with importing a dataset from Kaggle. To find the best model, the project compares performance of models trained using Automated ML and one customized model whose hyperparameters are tuned using HyperDrive in the Microsoft Azure's ecosystem. The project wraps up with deploying the best model and testing its endpoint.

## Project Set Up and Installation
> *OPTIONAL:* If your project has any special installation steps, this is where you should put it. To turn this project into a professional portfolio project, you are encouraged to explain how to set up this project in AzureML.

## Dataset

### Overview
> *TODO*: Explain about the data you are using and where you got it from.

This project processes a data set describing the sale of individual residential property in Ames, Iowa from 2006 to 2010. The data set contains 2930 observations and a large number of explanatory variables (23 nominal, 23 ordinal, 14 discrete, and 20 continuous) involved in assessing home values. The Ames Housing dataset was compiled by Dean De Cock for use in data science education.

### Task
> *TODO*: Explain the task you are going to be solving with this dataset and the features you will be using for it.

The project's goal is to train and deploy a machine learning model for prediction of the sales price based on parameters of a house. The `train_xgb.py` module encodes data types of categorical variables, imputes missing values and cleans the data in line with findings of an exploratory data analysis. There is no additional feature used in this iteration.

### Access
> *TODO*: Explain how you are accessing the data in your workspace.

The Ames Housing dataset is downloaded from Kaggle.com by `train_xgb.load_data_clean(source='kaggle')` and registered to the workspace. The HyperDrive child runs use the `train.csv` file saved locally after the download to prevent "Too many request" error from Kaggle (`train_xgb.load_data_clean(source='local')`).

## Automated ML
> *TODO*: Give an overview of the `automl` settings and configuration you used for this experiment

![AutoML Settings and configuration](http://www.plantuml.com/plantuml/png/RLLHRnit37xtho0mO6bJs5YxxcLeYmRB0WpOt64Dkhq9z8bd2zM9DubdrstttqVfT50G5qaSwyZl8_cHrBrDWb4IUbbzMMqsgzTmCmd_yVil77gtNtsv_su5htPlHemua524h_buH3_H_3MmqEeP2AQF-k0gqZvIIex3bHxbG23daO3xsKCOuXJKVunkm7WsIXfTbv61uu3UVIPh8hEe1OD9_quOzGd5o75Xh9YU8mnioKCYJvqupiGT3-CaP0JZdaGHx-zljhStVzsQsnVcmmlu7bwgZ-POoQe_LFyvmMAXJoDfbXG42hD4TC65lR4egEW3JudMewP2QOtsYA4Zksu2R3QR6cD1Ga4-wGbboXbWi83WSKV-QOwy8r1A2oSd1_Su2SsWU9gE_JG44t2WhDjxzFHdJk8AQhXYuNwXXXa0BbmciuBhQvo41syIYUZZwsiDrA8QqNyyQJjScAIezlp53_evu2StJ0Dak_AY07eFJYXYxaJAmkvS80iTQc3yI5gUjemUQwi8vKRbri31T95JCZfWpbQYh_1ZKVkaCSCPYWCqXooSaYdr0AS3XInXV6Wlehi4WGNII9th7TbSPC2T9qCO_TaauN7KyZNIVIopFPkXc9Sa2v_hImafJz72wuOnyZ7ZNP3PVE0u5xTwrcJvXfm_VLDCmkxGO4N3E8L5GlT8DiNhM8HkYZ7thE0MyLxgdoOpUQjeyAJYIPQ98v1kbmVXal2IGvY67SKyFu5jOyyhOrJdHgwyw-UWdofuRdvX6JabfxhL7LD0gwASkeFpTZrV0gywzXn_reKvlwdTu11oi65KH3wN1SzbFFIj7Rg40mNLfzC-b6JURRV_h1iPp6HvvYtrE7c1ElIfJFsyb-xpKjrLtenwwJmo9g5HrzJxhAdbG52sI8sTAd5MiZaJAWtNgip91SkdrEQhEW3ENVTkS08SvYJRbbxEWlx-FPELJUtyPCa43APiUukms22gQxbJO8jRA7TtMcw3Wb6U8yKT9oTdnUNzBiP59Kz7ykM-FKKdHLsUqRo7tdc29ufv_Hf-szwzUzfMItebkaEVSZQMnaWT2bbeRnFbiIwLrjrJI1pllEuv-Zr7pNVG2cSzZ5uO7ftIEgz9NcnfDI-Dtr6I-YAhUg8K0mLRRaRlgxa9tPQc5N1aKPFHp6ZGyqNO3yN-QpKt2cMmj9lsHWLQ1cdm6ptLSMhA2HTHQGQ0orCnB1TRoyHpXzuC671FjgcwgFTGqpKKPrYSunHIkK02YofJ6UqiYKjb_5eW6y93UYue5-P9kjrkOOT9mNKlxHHLW8lNy7_wyrQrJkZbVm00)

*Figure 1: Overview of the AutoML Configuration*

As there are time constraints for the experiment, the automl setting:

+ sets experiment timeout to 2 hours,
+ enables early stopping,
+ disables the neural networks (this is a default setting).

Number of cross validation is set to 3 as the dataset has more then 1.000 data points. For the sake of cross platform migration, the ONNX compatible models are enabled.

### Results
> *TODO*: What are the results you got with your automated ML model? What were the parameters of the model? How could you have improved it?

> *TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Hyperparameter Tuning
> *TODO*: What kind of model did you choose for this experiment and why? Give an overview of the types of parameters and their ranges used for the hyperparameter search

The HyperDrive experiment uses XGBoost regressor which has been the best performing model from the voting ensemble crafted by the AutoML experiment. Hyperparameters tuned are:
+ `learing_rate` alias `eta` is the step size shrinkage used in update to prevent overfiffing, its range is [0,1] and for search are used values in interval [0.01, 0.2] with log scale,
+ `gamma` specifies the minimum loss reduction required to make a further partition on a leaf node of the tree; the larger `gamma` is, the more conservative the algorithm will be; its range is [0,∞] and for search is used interval [0,9]
+ `max_depth` is maximum depth of a tree, increasing this value will make the model more complex and more likely to overfit; its range is [0,∞] and for search are used values 3, 5, and 7.

These are Tree Booster parameters. Other parameters are left with their default values except a learning parameter `objective` which takes value `reg:squarederror`.

### Results
> *TODO*: What are the results you got with your model? What were the parameters of the model? How could you have improved it?

> *TODO* Remeber to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Model Deployment
*TODO*: Give an overview of the deployed model and instructions on how to query the endpoint with a sample input.

## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:
- A working model
- Demo of the deployed  model
- Demo of a sample request sent to the endpoint and its response

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
