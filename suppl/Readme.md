# Predict House Prices - Supplement
## To-Dos
- [x] ipynb > ACI deployment: in `myenv = Environment.get(workspace=ws, name="project-env", version="1")` delete `, version="1")`
- [ ] xgb: Emphasize the effects of the different hyperparemeters on the primary metric of your model
- [x] Readme: Provide short overview of how to improve the project in the future
- [ ] Take screenshots: 
  - RunDetails, performance of different models and the best models (aml + hdr | sdk + gui), 
  - the model endpoint is active (sdk + gui), 
  - the logs and metrics of a web service
- [ ] Screencast: working model, deployed model, sample request and response, application insights, prd

## ACI Deployment Failures
### Errors
**Context**: The Python SDK in Azure ML Studio is running `Model.deploy()` method as in [MS Docs: Deploy again and call your service](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python#deploy-again-and-call-your-service) or [MS Docs: Deploy in ACI](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-deploy-models-with-aml#deploy-in-aci).

**Error** while "Checking the status of inference endpoint ames-housing-aml-xxxx." (2021-08-17, Optimizing an ML Pipeline Project Lab's Workspace | 2021-08-18, Machine Learning Operations Project Lab's Workspace | 2021-08-19 Capstone Project Lab's Workspace):

```
Service deployment polling reached non-successful terminal state, current service state: Failed
Operation ID: e29418d6-3866-4603-91f8-0b2cb756ebc1
More information can be found using '.get_logs()'
Error:
{
  "code": "AciDeploymentFailed",
  "statusCode": 400,
  "message": "Aci Deployment failed with exception: Your container application crashed. This may be caused by errors in your scoring file's init() function.
	1. Please check the logs for your container instance: ames-housing-aml-0812. From the AML SDK, you can run print(service.get_logs()) if you have service object to fetch the logs.
	2. You can interactively debug your scoring file locally. Please refer to https://docs.microsoft.com/azure/machine-learning/how-to-debug-visual-studio-code#debug-and-troubleshoot-deployments for more information.
	3. You can also try to run image c726cd197c8d4e64902174bc769dc498.azurecr.io/azureml/azureml_e434aed78f9426216c7e0e89c0851446 locally. Please refer to https://aka.ms/debugimage#service-launch-fails for more information.",
  "details": [
    {
      "code": "CrashLoopBackOff",
      "message": "Your container application crashed. This may be caused by errors in your scoring file's init() function.
	1. Please check the logs for your container instance: ames-housing-aml-0812. From the AML SDK, you can run print(service.get_logs()) if you have service object to fetch the logs.
	2. You can interactively debug your scoring file locally. Please refer to https://docs.microsoft.com/azure/machine-learning/how-to-debug-visual-studio-code#debug-and-troubleshoot-deployments for more information.
	3. You can also try to run image c726cd197c8d4e64902174bc769dc498.azurecr.io/azureml/azureml_e434aed78f9426216c7e0e89c0851446 locally. Please refer to https://aka.ms/debugimage#service-launch-fails for more information."
    },
    {
      "code": "AciDeploymentFailed",
      "message": "Your container application crashed. Please follow the steps to debug:
	1. From the AML SDK, you can run print(service.get_logs()) if you have service object to fetch the logs. Please refer to https://aka.ms/debugimage#dockerlog for more information.
	2. If your container application crashed. This may be caused by errors in your scoring file's init() function. You can try debugging locally first. Please refer to https://aka.ms/debugimage#debug-locally for more information.
	3. You can also interactively debug your scoring file locally. Please refer to https://docs.microsoft.com/azure/machine-learning/how-to-debug-visual-studio-code#debug-and-troubleshoot-deployments for more information.
	4. View the diagnostic events to check status of container, it may help you to debug the issue.
"RestartCount": 3
"CurrentState": {"state":"Waiting","startTime":null,"exitCode":null,"finishTime":null,"detailStatus":"CrashLoopBackOff: Back-off restarting failed"}
"PreviousState": {"state":"Terminated","startTime":"2021-08-19T06:24:07.256Z","exitCode":111,"finishTime":"2021-08-19T06:24:13.387Z","detailStatus":"Error"}
"Events":
{"count":2,"firstTimestamp":"2021-08-19T06:18:58Z","lastTimestamp":"2021-08-19T06:22:20Z","name":"Pulling","message":"pulling image "c726cd197c8d4e64902174bc769dc498.azurecr.io/azureml/azureml_e434aed78f9426216c7e0e89c0851446@sha256:f108f3922cd028c69f1560739e46003bcf3560a181056de8621ed8ec237a3057"","type":"Normal"}
{"count":2,"firstTimestamp":"2021-08-19T06:22:20Z","lastTimestamp":"2021-08-19T06:22:20Z","name":"Pulled","message":"Successfully pulled image "c726cd197c8d4e64902174bc769dc498.azurecr.io/azureml/azureml_e434aed78f9426216c7e0e89c0851446@sha256:f108f3922cd028c69f1560739e46003bcf3560a181056de8621ed8ec237a3057"","type":"Normal"}
{"count":4,"firstTimestamp":"2021-08-19T06:22:34Z","lastTimestamp":"2021-08-19T06:24:07Z","name":"Started","message":"Started container","type":"Normal"}
{"count":4,"firstTimestamp":"2021-08-19T06:22:39Z","lastTimestamp":"2021-08-19T06:24:13Z","name":"Killing","message":"Killing container with id 66ba6b84d7282b5366c98e93782b19716a0da22f87ecf844a4f813ffe9753c32.","type":"Normal"}
"
    }
  ]
}
```

Note: The error above occured only when deploying the AutoML model. The XGB/hdr model was deployed successfully!

### Analysis
**Observations**:
+ The return value of service.get_logs() is None.
+ No same or similar problem found in the Internet search (StackOverflow, Udacity Help Forum et al.).
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

**Enable Docker** Trial: 

As the problem origins from an environment within Azure Container Instance (ACI), its cause is most probably in an environment setup. Try [Enable Docker](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-environments#enable-docker) before registering the environment:

```
# Creates the environment inside a Docker container.
env.docker.enabled = True
```

2021-08-17: This setting displays warnning: 'enabled' is deprecated. Please use the azureml.core.runconfig.DockerConfiguration object ([StackOverflow: How to use it](https://stackoverflow.com/questions/67387249/how-to-use-azureml-core-runconfig-dockerconfiguration-class-in-azureml-core-envi)) with the 'use_docker' param instead. Furthermore, it doesn't eliminate the AciDeploymentFailed error.

Another tip: Create more complete environment with `CondaDependencies.create()` as in [Github: Image Classification Tutorial](https://github.com/Azure/MachineLearningNotebooks/tree/master/tutorials/image-classification-mnist-data) for example.


# References
+ [MSDocs: Troubleshooting remote model deployment](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-troubleshoot-deployment?tabs=python)
+ [MSDocs: Troubleshooting with a local model deployment](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-troubleshoot-deployment-local)
+ [MSDocs: What are Azure Machine Learning environments?](https://docs.microsoft.com/en-us/azure/machine-learning/concept-environments)
---
+ [Udacity: Optimizing an ML Pipeline in Azure Project Review](https://review.udacity.com/#!/reviews/3017477)
+ [Udacity: Operationalizing Machine Learning Project Review](https://review.udacity.com/#!/reviews/3053642)

# Appendix

**Error** while "Checking the status of inference endpoint xxx" (2021-08-16, Capstone Project Lab's Workspace). This error occured only once in a scenario, when the deployment of AutoML Model comes first. Then the same failure ended up the XGB model deployment:

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
