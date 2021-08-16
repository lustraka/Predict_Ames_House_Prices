# Predict House Prices - Supplement
## To-Dos
- [ ] ipynb > Dataset: Correct articles and word order.
- [ ] xgb.ipynb: Provide details of the best model (and document the parameters of that model)
- [ ] xgb: Emphasize the effects of the different hyperparemeters on the primary metric of your model
- [ ] Readme: Provide short overview of how to improve the project in the future
  - [ ] Use feature engineering
  - [ ] Enable neural networks and deep learning
  - [ ] Use pipelines
  - [ ] Use Bayesian sampling for more profound hyperparameter sampling
  - [ ] Learn how to retrain and re-deploy the model
- [ ] Take screenshots: 
  - RunDetails, performance of different models and the best models (aml + hdr | sdk + gui), 
  - the model endpoint is active (sdk + gui), 
  - the logs and metrics of a web service
- [ ] Screencast: working model, deployed model, sample request and response, application insights, prd

## Service Deployment Failure (ModuleNotFoundError, 2021-08-16)
**Context**: The Python SDK in Azure ML Studio is running `Model.deploy()` method as in [MS Docs: Deploy again and call your service](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python#deploy-again-and-call-your-service) or [MS Docs: Deploy in ACI](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-deploy-models-with-aml#deploy-in-aci).

**Error** while "Checking the status of inference endpoint xxx":

```
ERROR:azureml.core.webservice.webservice:Service deployment polling reached non-successful terminal state, current service state: Unhealthy
Operation ID: 238ed8fc-ce62-4929-a516-3ac8ad5de684
More information can be found using '.get_logs()'
Error:
{
  "code": "AciDeploymentFailed",
  "statusCode": 400,
  "message": "Aci Deployment failed with exception: Error in entry script, ModuleNotFoundError: No module named 'azureml.api', please run print(service.get_logs()) to get details.",
  "details": [
    {
      "code": "CrashLoopBackOff",
      "message": "Error in entry script, ModuleNotFoundError: No module named 'azureml.api', please run print(service.get_logs()) to get details."
    }
  ]
}
```

**Analysis**:
+ An entry script proved working well in previous runs and no object from 'azureml.api' occurs in its code.
+ The return value of service.get_logs() is None.
+ Deployment was successful in previous runs. Difference is in the virtual machine environment (various Udacity Labs).
+ No same or similar problem found in the Internet search (StackOverflow et al.).
+ An initial set up of the inference config environment:

```
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies

env = Environment("project-env")
cd = CondaDependencies('aml-outputs/conda_env_v_1_0_0.yml')
env.python.conda_dependencies = cd
# Register environment to re-use later
env.register(workspace=ws)
```

**Solution** Proposals: 

As the problem origins from an environment within Azure Container Instance (ACI), its cause is most probably in an environment setup. Try:
+ [Enable Docker](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-environments#enable-docker) before registering the environment:

```
# Creates the environment inside a Docker container.
env.docker.enabled = True
```

+ Create more complete environment with `CondaDependencies.create()` as in [Github: Image Classification Tutorial](https://github.com/Azure/MachineLearningNotebooks/tree/master/tutorials/image-classification-mnist-data) for example.


# References
+ [Optimizing an ML Pipeline in Azure Project Review](https://review.udacity.com/#!/reviews/3017477)
+ [Operationalizing Machine Learning Project Review](https://review.udacity.com/#!/reviews/3053642)
