# Build your own Machine Learning application with Amazon SageMaker, AWS Glue and Amazon API Gateway

## Introduction

The Machine Learning process is an iterative process that consists of several steps:

- Identifying a business problem and the related Machine Learning problem
- Data ingestion, integration and preparation
- Data visualization and analysis, feature engineering, model training and model evaluation
- Model deployment and deployed model monitoring and debugging

The previous steps are generally repeated multiple times to better meet business goals following to changes in the source data, decrease in the perfomance of the model, etc.

The process can be represented with the following diagram:

<img src="images/ml_process.png" alt="ML Process" width="700px" />


After a model has been deployed, we might want to integrate it with our own application to provide insights to our end users.

In this workshop we will go through the steps required to build a fully-fledged machine learning application on AWS. We will execute an iteration of the Machine Learning process to build, train and deploy a model using Amazon SageMaker and AWS Glue, and then we will add inference capabilities to a demo application deploying a REST API with Amazon API Gateway.

The final architecture will be:

[insert architecture diagram]

## The Machine Learning task

Bla bla bla

## Modules

This workshops consists of six modules:

- <a href="01_create_notebook_instance/">**Module 01**</a> - Creating an Amazon SageMaker managed Jupyter notebook instance and an Amazon S3 bucket that will be used for storing data, models and code. 
- <a href="02_data_exploration_and_feature_eng/">**Module 02**</a> - Using AWS Glue and Amazon Athena to execute data preparation and data exploration, and then feature engineering using SparkML.
- <a href="03_train_model/">**Module 03**</a> - Training a binary classification model using Amazon SageMaker built-in XGBoost algorithm, that will predict whether a wind turbine plant requires maintenance.
- <a href="04_deploy_model/">**Module 04**</a> - Deploying the feature engineering and ML models as a pipeline using Amazon SageMaker hosting.
- <a href="05_API_Gateway_and_Lambda/">**Module 05**</a> - Buiding a REST API using Amazon API Gateway and implementing an AWS Lambda function that will invoke the Amazon SageMaker endpoint for inference.
- <a href="06_invoke_API/">**Module 06**</a> - Using a single-page demo application to invoke the REST API and get inferences.

You must comply with the order of modules, since the outputs of a module are inputs of the following one.

## Getting started

This workshop has been designed assuming that each participant is using an AWS account that has been provided and pre-configured by the workshop instructor(s). However, you can also choose to use your own AWS account, but you'll have to execute some preliminary configuration steps as described <a href="setup/">here</a>.

Once you are ready to go, please start with <a href="01_create_notebook_instance/">**Module 01**</a>.

## License

The contents of this workshop are licensed under the [Apache 2.0 License](./LICENSE).

## Authors

[Giuseppe Angelo Porcelli](https://it.linkedin.com/in/giuporcelli) - Principal, ML Specialist Solutions Architect - Amazon Web Services EMEA<br />
[Antonio Duma](https://it.linkedin.com/in/antoniod82) - Solutions Architect - Amazon Web Services EMEA