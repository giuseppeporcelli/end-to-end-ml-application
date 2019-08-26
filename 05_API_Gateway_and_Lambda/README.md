# Build a REST API with Amazon API Gateway and AWS Lambda

Once we have trained our model and deployed to an Amazon SageMaker fully-managed endpoint, we are ready to build a REST API that will be invoked by client applications to get inferences.
Although the Amazon SageMaker HTTPs endpoint might be called directly, using Amazon API Gateway for our REST API provides more control on things like user authorization, usage profiles, throttling, API versioning, etc. 

The request flow would be:

1. The client application executes a POST request to the Amazon API Gateway endpoint
2. An AWS Lambda function processes the request and calls the Amazon SageMaker HTTPs endpoint where our model is hosted
3. The inference response is returned by the Amazon SageMaker endpoint and sent back to the client via Amazon API Gateway

Let's get started by creating our rest API.

## Create AWS Lambda function and Amazon API Gateway REST API

We are going to use AWS Cloud9 for building our API: AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. The service preconfigures the development environment with all the SDKs, libraries, and plug-ins needed for serverless development, thus facilitating the development of AWS Lambda functions and API Gateway APIs.

1. Open your **AWS Console** and open **Cloud9**
2. Click on **Create environment**
	
	<img src="images/cloud9_dashboard.png" alt="Cloud9 Dashboard" width="700px" />

3. Add a name **endtoendml-env**, click on **Next step**
4. Leave the configuration with the default settings and click on **Next step**
5. Click **Create environment**

	Now that we have created our Cloud9 environment we will be waiting a couple of minutes for the environment to be up and running and in front of us.

	<img src="images/cloud9_loading.png" alt="Cloud9 Loading" width="700px" />

Once the environment is up and running please:

1. Press on **AWS Resources** on the right side of the screen
2. Click on the **Lambda icon** to create a new function as it is shown on the picture below.

	<img src="images/cloud9_new_function.png" alt="Cloud9 New Function" width="700px" />

3. Type **endtoendmllambdafunction** in the function name textbox and **endtoendmlapplication** in the application name textbox and click **Next**.
4. Select **Python3.6** in runtime. Then chose **enpty-python** and click **Next**.
5. In Function trigger, leave none and click **Next**.
6. In the **Create serverless application** window, select _Choose existing role_ in the **Role** dropdown and then choose the IAM role _LambdaInvokeSageMaker_ for the **Existing Role** dropdown. This will allow the function to invoke the Amazon SageMaker endpoint. Then press **Next**.
	
	> The **LambdaInvokeSageMaker** IAM role has been created in advance in your AWS account for the purpose of this workshop.
7. Press **Finish**.
8. Once clicked on **Finish** you _might_ get a pop up window asking for **Drag & drop files here**, in this case, please ignore it by click on **x** on the top right corner of the popup window.

Now that we have created our Lambda function, we need to add the code to it. The files that we are going to edit are _lambda__function.py_ and _template.yaml_ that you can open using the file browser in the left side of the Cloud9 editor.

<img src="images/cloud9_tree.png" alt="Cloud9 tree" width="700px" />

### Edit _lambda__function.py_

The file _lambda__function.py_ will contain the code that will process the content of the HTTP request of the API call and invoke the Amazon SageMaker endpoint.

Please **replace** the content of that file with the following snippet, making sure that the indentation is matching:

```
import boto3
import json
import csv
import os

ENDPOINT_NAME = 'predmain-sk-ll-endpoint'
runtime= boto3.client('runtime.sagemaker')

def build_response(status_code, response_body):
    return {
                'statusCode': status_code,
                'body': json.dumps(response_body),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Access-Control-Allow-Credentials' : 'true',
		            'Access-Control-Allow-Headers': '*'
                },
            }

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    if 'httpMethod' in event:
        if event['httpMethod'] == 'OPTIONS':
            return build_response(200, '')

        elif event['httpMethod'] == 'POST':
            turbine_data = event['body']
            
            response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                               ContentType='text/csv',
                                               Body=turbine_data)
            print(response)
            result = json.loads(response['Body'].read().decode())
            print(result)
            return build_response(200, result)
    
        else:
            return build_response(405, 'null')

```
The implementation is straightforward: the Lambda handler can manage both OPTIONS and POST requests, and when a POST is executed, the Amazon SageMaker endpoint is invoked with the _Body_ parameter set to the request body. Then, the response is returned to the caller.

Please note that the **ENDPOINT_NAME** variable has been set to the name of the endpoint that was deployed in the previus module of this workshop.

### Edit _template.yaml_
The file _template.yaml_ contains a template - defined through the **Serverless Application Model** - to deploy the AWS Lambda function. We are going to add a few instructions to deploy also an Amazon API Gateway API.

Please **add** the following lines to the _template.yaml_ file, after the _CodeUri_ property, making sure that the _Events_ property indentation is matching the indentation of _CodeUri_:

```
      Events:
        GetInference:
          Type: Api
          Properties:
            Path: /
            Method: POST
        OptionsInference:
          Type: Api
          Properties:
            Path: /
            Method: OPTIONS
```
The additional statements are used to deploy an Amazon API Gateway REST API, which will accept POST and OPTIONS requests and pass the request content to the AWS Lambda function defined above.

For additional information on this way of integrating AWS Lambda and Amazon API Gateway, please visit <a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html">**AWS Lambda Proxy Integration**</a>.  


### Test locally

sddsds

### Deploy function and API

sddsds

## Invoke the API from a client application

sddsds

