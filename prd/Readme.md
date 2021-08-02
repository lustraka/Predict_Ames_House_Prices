# Ames Housing Azure ML Product Requirements Document
**Author**: Lubomir Straka [LS]
> A product requirements document (PRD)  is a guide that defines a particular **product’s requirements**, including its purpose, features, functionality, and behavior. This document is generally written by the Product Manager to communicate **what** they are building, **who** it is for, and **how** it benefits the end-user. It also serves as a guide for business and technical teams to help **develop, launch, and market** the product.

# Change History
> A PRD is a living document that should be continuously updated according to the product’s lifecycle.
+ 2021-07-28 LS starts writing product requirements for the Ames ML experiment.

# Overview
> Briefly, what is this project about?  Why are you doing it?

A value proposition of the **Ames Machine Learning Experiment** has three levels, let's call them context, content, and code levels.
+ A **context (strategy) level** offers an example of a data science solution to a business problem. It approaches a machine learning solution as a business product or contract that needs a technical specification which is clear, concise, testable, traceable, and correct.
+ A **content (story line) level** is about one of the canonical data mining tasks. The goal of the project on this level is to estimate or predict sale prices of houses in Ames with a regression model trained on historical data. The Ames Housing dataset is downloadable from Kaggle.com. It is located in House Prices Advanced Regression Techniques ongoing competition connected with one of Kaggle's tutorials.
+ A **code (procedural) level** serves the need of passing the capstone project assignment in Udacity Machine Learning Engineer for Microsoft Azure Nanadegree Program. This level determines application and infrastructure components of the data science solution.

![Value Proposition of the Product](http://www.plantuml.com/plantuml/png/TP9VYnen5CNVyobIAJX2XxuN4Mqhj511EhHFWiJaejdDdo7tHlJRR-uuhhhgIp39-NdEFPafaagKlHEVRD0k6v1ZbVJEUaNmTNR-DH5YE7VW8H2AHIIxLsHZM3UaNc4NdO5KsR07f9Y-oC5FHKessaBGi0g_-ul1w1cQG6qXK27dICLEpifM7rUXAkvR6y2CdiCSgdFzPvIsT9GB27Tk_vNBK1b4k8lNH9TP8-S7vLi7Zq2rmxOjvCm3obynemtRGYe7SfcivXMCrKmymhDkyIhW3zKYnL2yboc-W2RPv8stY2VyE_yz8AxBhScQAkKTdiqNVqhE5fBbiOjO3F-2wxnGd5z0rhNaKKNVA--x2KI1-dkE95Z46pQGtwIEWU10ejD-F0yacBavDY24Ws9XnFZpvRFnx_FNU7ceIK6ktcr5Jv0zLyRYhhjRsQQlfcvFrR2iRqcK5B8FCorBzkuD)

*Figure _: Value Proposion of the Ames ML Experiment*

# Success Metrics
> What are the success metrics that indicate you’re achieving your internal goals for the project?
+ **Customer Conversion Rate**: number of jobs won through reference to this portfolio project.
+ **RMSLE**: performance of the model, also score in a Kaggle competition.
+ **Project Pass**: passing the capstone project in Udacity Machine Learning Engineer with Microsoft Azure Nanodegree Program.

# Messaging
> What’s the product messaging marketing will use to describe this product to customers, both new and existing?

**Check in data science, check out business needs!**

# Timeline/Release Planning
> What’s the overall schedule you’re working towards?

The deadline for the capstone project is Sep 3, 2021.

# Personas
> Who are the target personas for this product, and which is the key persona?

## Businessman Investing in Data Science Ventures
Linda Dillman is a mid-age business-woman with a fresh start-up mindset. She is a humble, kind person who treats everyone with respect. She is generous with her time, money and gentle advise. Her smile is infectious, and her laugh will fill the room. She enjoy reading, spending time with family and friends. She travels a lot, both for business and pleasure, leaving behind a wide range of admirers in the form of friend, acquaintances and business associates all over the world.

Linda is a chief information officer in a global retail company. She is trying to use information technology to improve efficiency of her business and unlock future organic growth potential. She knows, it is mainly about the extraction of useful information and knowledge from large volumes of data, in order to improve business decision-making. She is frustrated by the gap between quickly growing offerings of data science tools on the market and a shortage of talents necessary to take advantege of big data and data mining.

## Machine Learning Engineer
<!-- https://www.hunzikerrealty.com/ | https://jobbio.com/real-estate-webmasters | https://visionone.co.uk/brand-archetypes/the-creator-brand-archetype/ -->
Ross Hunziker is an experienced real estate webmaster who loves new ideas and gets deep satisfaction from both the process and the outcome of creating web services. He always tries to leave his comfort zone behind and make decisions that looks odd. He is good at coming up with lots of ways to solve problems. He is motivated to aquire new levels of knowledge, or deepen his existing knowledge or skills in a significant way.

Ross has been building a website helping buy and sell homes in Ames and Central Iowa for a couple of years. His property search tool provides access to a database of real estate listings by type, price, neighborhood, school district, and even number of bedrooms and bath. Now he wants to deploy a home value calculator which will provide an instant estimate of a property's value for those users who are considering buying or purchasing a house or refinancing their existing property.

## Udacity Mentor

Elisa Romondia is in the Forbes list "60 Women-Led Startups That Are Shaking Up Tech Across The Globe". In her words, "The most rewarding aspect of being a Udacity Mentor for me is to mentor students from across the world, being part of an inclusive community of highly specialized mentors always ready to share and support."

Elisa provides personalized feedback and responses to support students to learn and grow. Her feedback is also accurate, as she refers back to classroom content or items in a knowledge base. Her reviews are written in accesible language and contain useful resources where relevant. She reviews each rubric item, check previous reviews, and read student notes to thoroughly address every aspect of a submission.

# User Scenarios
> These are full stories about how various personas will use the product in context.

![ML Workflow](http://www.plantuml.com/plantuml/png/RSz1Zi8m30NGVKxXSsH6euxe0YHOqGkOnfI898uS5zJROq5XnIxvUlhwxfgYw9oJyqTAD2eW15HifB_Ext9bKT0BlKE8HHdkBDTMSQGVrsgAwlmW60ja3fHWRh5CxdzMpgWKuB1V6U1awXlUBfMabtYpHYe1rjODvuf2ApLoPibOHbE-fvfuUMuxKTENiNpuVC2QAjlWFzVPquvy0000)

*Figure _: Ames ML Experiment Workflow*

# User Stories/Features/Requirements
> These are the distinct, prioritized features along with a short explanation as to why this feature is important.

When an ML experiment is about to start, an ML engineer shall:
+ sign in to Azure workspace, 
+ open Azure ML Studio,
+ create a compute instance to run Jupyter notebooks,
+ upload source code (Jupyter notebooks and Python scripts) from the experiment's GitHub repository to the workspace.

While building a dataset, an Ames ML Experiment shall:
+ download Ames Housing dataset from Kaggle website,
+ upload train and test dataset to the workspace,
+ clean the dataset,
+ augment the dataset using feature engineering (where feature engineering is included),
+ register the dataset into the workspace.

While training model using Automated ML, an Ames ML Experiment shall:
+

While training model using HyperDrive, an Ames ML Experiment shall:
+

While deploing the best model, an Ames ML Experiment shall:
+


![The Product and Key Deliverables](http://www.plantuml.com/plantuml/png/XPHlQzi-4CUV-rNeLtwioQYTvwEKfcjXWwqBsVQWO32AT7MqofAgFsKPU_6xKzmwR7Rp93fnd-zP5trrbo5o7rEdY_-K4Jf9OEVSYwtgU8J5yZcwA8hJ6mqTc1YAgnIKWH2QbRSoYJZZdGvdx6JPGM2VFx6Rdmwy8lPaFi3lhOcU8-syHBZNiZKy9kNtbMjpRKMYaCrMw-lveVpBvWUWE7fmgFu6OckKu1hrplfuLXiwViKaE6rtkKJ7JU8QQooTqyX6PKrppIFlImLXwI1VRV8266wWDhFLtHdxkBgxlPfF2_bMlhJxmT81szf8p0UWZlFPhBRjhbdwgExxdds76bmNQ-2oWwgJ4sm6Zq6y0pe3BPNRiJUreR2v1znDILAqdIPH3YhbTcOpmMvtBYA92tZ7FTQEu9lQn6GCjlkgDdgk38hpMedmDCL1e6_GyYzrQoNCMXMtQMCmH6w_gOJj5Ze5BFx05xLPUP1An6P9tTDb0BfI2GWZvHvussegjGzoAO4rjYGhNPQLN3vn8q2MjV7GUWX1MLF6xBV716515ut5YzCrw6oDK93_sTkoPCxBOKDM7NRajc575YfE4MVdlwkAPNiKMB1P0zVgrzvotrtl6yhFnzAKey-C9hD5wBlZsjuEqm1vO3hTNtFkP3mF8Hwcbo6erj3BfEpXrUOcZq772UhtA9ERFaPHvsFCiu5owwy24B10eQ458ulp_uU9kkddMUdsy--2lMFzAApZA2ZwkKbaFqEdK9ld4u7FOvFjHrRzbu8FWwqaFnyebqEAqSnxgN2eZoylg-JzSyxQ71FC9cZwVucazrZ70ena_PzqYJ-fqty0)

*Figure _: Key Deliverables of the Ames ML Experiment*

# Features Out
> What have you explicitly decided not to do and why

# Designs
> Include any needed early sketches, and throughout the project, link to the actual designs once they’re available.

![State Diagram](http://www.plantuml.com/plantuml/png/VPA_Rjum3CHtFGMHeKE13FMOeKYBZitKRd46sRgl5g0_gaW7i9--z6SfHP4cWmSTZxyx0xndiLNM6CpY7GYno4OEF5TVnETaT2wWcwyh-mJcCPMQfu0u9eUBIkw6BDDa7Zy-qUrdckYEpW790denSy7iBnjL_5vzHKGIxknlLYn3nbJnoxEWDgWpqu5qYfnM7zoOBBdJsrU_h98VlbFC3e6asfT2KJvrpmy4p0BNNBc8ZtxllZmO_UvesGfgiTL622gJh8fw0_5lq60StMfFZTIc5o_zdGTz7vmZeLc6PlbVVppRi5hfOBpwWpTyWz7eau-Z0i-vGhMMYU6l1lKzEiiBt5Dlo5Twp_gvW2QmZEaQDgPptCBAYL1iqSqvnsAlsE6Lrd0F9yIXXBmrI3Q5r9tLVUhl71ddyDpMTfEFjLtN12pquJYOagkO_T3r0CqzajDR_WC0)

*Figure _: State Diagram of the Ames ML Experiment*

# Open Issues
> What factors do you still need to figure out?

# Q&A
> What are common questions about the product along with the answers you’ve decided? This is a good place to note key decisions.

# Other Considerations
> This is a catch-all for anything else, such as if you make a key decision to remove or add to the project’s scope.

# References
+ [Udacity: Machine Learning Engineer for Microsoft Azure Nanodegree Program](https://www.udacity.com/course/machine-learning-engineer-for-microsoft-azure-nanodegree--nd00333)
+ [Kaggle: House Prices - Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
+ [ProductSchool: Product Requirements Document (PRD)](https://productschool.com/blog/product-management-2/product-template-requirements-document-prd/)
+ [JamaSoftware: How to Write an Effective Product Requirements Document](https://www.jamasoftware.com/blog/how-to-write-an-effective-product-requirements-document)
+ [EARS – The Easy Approach to Requirements Syntax](https://qracorp.com/easy-approach-to-requirements-syntax-ears-guide/)
+ [Udacity: Capstone - Azure Machine Learning Engineer - Project Specification](https://review.udacity.com/#!/rubrics/2864/view)
+ [MS Docs: What is automated machine learning (AutoML)?](https://docs.microsoft.com/en-us/azure/machine-learning/concept-automated-ml?view=azure-ml-py)
+ [MS Docs: Hyperparameter tuning a model with Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-tune-hyperparameters?view=azure-ml-py)
+ [MS Docs: Consume an Azure Machine Learning model deployed as a web service](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-consume-web-service?view=azure-ml-py&tabs=python#call-the-service-python)
+ [MS GitHub: Training of Python scikit-learn models on Azure Example](https://github.com/microsoft/MLHyperparameterTuning)
+ 

<!--  -->
