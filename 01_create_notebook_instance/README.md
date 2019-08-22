# Create a managed Jupyter Notebook instance with Amazon SageMaker

## Overview

Amazon SageMaker is a fully-managed service that enables developers and data scientists to quickly and easily build, train, and deploy machine learning models at any scale. Amazon SageMaker removes all the barriers that typically slow down developers who want to use machine learning.

Machine learning often feels a lot harder than it should be to most developers because the process to build and train models, and then deploy them into production is too complicated and too slow. First, you need to collect and prepare your training data to discover which elements of your data set are important. Then, you need to select which algorithm and framework you’ll use. After deciding on your approach, you need to teach the model how to make predictions by training, which requires a lot of compute. Then, you need to tune the model so it delivers the best possible predictions, which is often a tedious and manual effort. After you’ve developed a fully trained model, you need to integrate the model with your application and deploy this application on infrastructure that will scale. All of this takes a lot of specialized expertise, access to large amounts of compute and storage, and a lot of time to experiment and optimize every part of the process. In the end, it's not a surprise that the whole thing feels out of reach for most developers.

Amazon SageMaker removes the complexity that holds back developer success with each of these steps. Amazon SageMaker includes modules that can be used together or independently to build, train, and deploy your machine learning models.

In this section, we will walk you through creating a fully-managed Jupyter Notebook instance with Amazon SageMaker, that will be used to execute our experimentation and build the Machine Learning model.

## Create an Amazon S3 bucket
In this section, we will create an Amazon S3 bucket that will be our storage area. Amazon SageMaker and AWS Glue can both use **Amazon S3** as the main storage for both data and artifacts.

1. Sign into the **AWS Management Console** at <a href="https://console.aws.amazon.com/">https://console.aws.amazon.com/</a>
2. In the upper-right corner of the AWS Management Console, confirm you are in the desired AWS region. For the instructions of these workshop we will assume using the **US East (N. Virginia)** [us-east-1], but feel free to change the region at your convenience: the only constraints are that we keep consistent the region settings for all services used and services are available in the selected region (please check).
3. Open the **Amazon S3** console at <a href="https://console.aws.amazon.com/s3">https://console.aws.amazon.com/s3</a> or choose the Amazon S3 service in the menu.
4.	In the Amazon S3 console, click the **Create Bucket** button. ![Amazon S3 create bucket](images/create_bucket.png | width=500)
5.	For the **Bucket Name**, type _endtoendml-workshop-**[your-initials]**_ in the text box and click Next (take note of the bucket name, it will be needed later for loading data in the notebook instance). Press **Next** to move to the next screen.
Note: if the bucket name is already taken, feel free to add an extra suffix.

	![Amazon S3 create bucket window](images/create_bucket_window_1.png | width=500)
6. Enable versioning of the objects in the bucket as shown in the screen below. This is not strictly required for the workshop, but it is a suggested best practice to ensure consistency and reproducibility of the experimentations.

	![Amazon S3 create bucket window](images/create_bucket_window_2.png | width=500)

	Press **Next** and then **Next** again leaving the settings as they are in the following screen.
7. Finally, click **Create Bucket** in the Review page.


## Create a managed Jupyter Notebook instance
We are now ready to create an Amazon SageMaker managed Jupyter notebook instance.
An **Amazon SageMaker notebook instance** is a fully managed ML compute instance running the <a href="http://jupyter.org/">**Jupyter Notebook**</a> application. Amazon SageMaker manages creating the instance and related resources. 

1. In the AWS Management Console, click on Services, type “SageMaker” and press enter.
	
	![Amazon SageMaker](../images/sm_1.png)
2. You’ll be placed in the Amazon SageMaker dashboard. Click on **Create notebook instance**.
	
	![Amazon SageMaker](../images/sm_2.png)
3. In the **Create notebook instance** screen

	![Amazon SageMaker](../images/sm_5.png)

	1. Give the Notebook Instance a name like _endtoendml-nb-**[your-initials]**_

	2. Choose **ml.t2.medium** as **Notebook instance type**
	3. Choose **Create a new role** in the **IAM role** dropdown list. Notebook instances require permissions to call other services including Amazon SageMaker, AWS Glue and Amazon S3 APIs. Choose **Specific S3 buckets** in the **Create an IAM role** window and input the name of the bucket that you have created in the previous section. Then click on **Create role**.
	
		![Amazon SageMaker](../images/sm_3.png)
		If you already had a role with the proper grants to access the newly created bucket, creating a new role is not mandatory and you can just choose to use the existing role.
	4. Keep **No VPC** selected in the **VPC** dropdown list
	5. Keep **No configuration** selected in the **Lifecycle configuration** dropdown list
	6. Keep **No Custom Encryption** selected in the **Encryption key** dropdown list
	7. Finally, click on **Create notebook instance**

4. You will be redirected to the **Notebook instances** screen
	
	Wait until the notebook instance is status is **In Service** and then click on the **Open** button to be redirected to Jupyter
	
	![Amazon SageMaker](../images/sm_4.png)
	
	![Amazon SageMaker](../images/sm_6.png)

## Download notebook and training code to the notebook instance

For the purpose of this workshop the code required to build and train the Machine Learning model is pre-implemented and available for download from GitHub.

As a consequence, in this section we will clone the GitHub repository into the Amazon SageMaker notebook instance and access the Jupyter notebook to run training.

1. Click on **New > Terminal** in the right-hand side of the Jupyter interface
	
	![Amazon SageMaker](../images/sm_7.png)

	This will open a terminal window in the Jupyter interface
	
	![Amazon SageMaker](../images/sm_8.png)

2. Execute the following commands in the terminal

	```bash
	cd SageMaker
	git clone https://github.com/giuseppeporcelli/smlambdaworkshop
	```
3. When the clone operation completes, close the terminal window and return to the Jupyter landing page. The folder **smlambdaworkshop** will appear automatically (if not, you can hit the **Refresh** button)

	![Amazon SageMaker](../images/sm_9.png)
	
4. Browse to the folder **smlambdaworkshop > training** and open the file **sms\_spam\_classifier\_mxnet.ipynb**
