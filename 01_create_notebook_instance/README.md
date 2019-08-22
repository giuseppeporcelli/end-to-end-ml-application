# Create a managed Jupyter Notebook instance with Amazon SageMaker

## Overview

Amazon SageMaker is a fully-managed service that enables developers and data scientists to quickly and easily build, train, and deploy machine learning models at any scale. Amazon SageMaker removes all the barriers that typically slow down developers who want to use machine learning.

Machine learning often feels a lot harder than it should be to most developers because the process to build and train models, and then deploy them into production is too complicated and too slow. First, you need to collect and prepare your training data to discover which elements of your data set are important. Then, you need to select which algorithm and framework you’ll use. After deciding on your approach, you need to teach the model how to make predictions by training, which requires a lot of compute. Then, you need to tune the model so it delivers the best possible predictions, which is often a tedious and manual effort. After you’ve developed a fully trained model, you need to integrate the model with your application and deploy this application on infrastructure that will scale. All of this takes a lot of specialized expertise, access to large amounts of compute and storage, and a lot of time to experiment and optimize every part of the process. In the end, it's not a surprise that the whole thing feels out of reach for most developers.

Amazon SageMaker removes the complexity that holds back developer success with each of these steps. Amazon SageMaker includes modules that can be used together or independently to build, train, and deploy your machine learning models.

In this section, we will walk you through creating a fully-managed Jupyter Notebook instance with Amazon SageMaker, that will be used to execute our experimentation and build the Machine Learning model.

## Create an Amazon S3 bucket
In this section, we will create an Amazon S3 bucket that will be our storage area. Amazon SageMaker and AWS Glue can both use **Amazon S3** as the main storage for both data and artifacts.

1. Sign into the **AWS Management Console** at <a href="https://console.aws.amazon.com/">https://console.aws.amazon.com/</a>

2. In the upper-right corner of the AWS Management Console, confirm you are in the desired AWS region. For the instructions of these workshop we will assume using the **US East (N. Virginia)** [us-east-1], but feel free to change the region at your convenience.

	> The only constraints for changing AWS region are that we keep consistent the region settings for all services used and services are available in the selected region (please check in case you plan to execute this workshop in another AWS region).

3. Open the **Amazon S3** console at <a href="https://console.aws.amazon.com/s3">https://console.aws.amazon.com/s3</a> or choose the Amazon S3 service in the menu.
4.	In the Amazon S3 console, click the **Create Bucket** button.
	<img src="images/create_bucket.png" alt="create bucket" width="500px" />
	
5.	For the **Bucket Name**, type _endtoendml-workshop-**[your-initials]**_ in the text box and click Next (take note of the bucket name, it will be needed later for loading data in the notebook instance). Press **Next** to move to the next screen.

	> **Note:** if the bucket name is already taken, feel free to add an extra suffix.

	<img src="images/create_bucket_window_1.png" alt="create bucket window 1" width="500px" />
	
6. Enable versioning of the objects in the bucket as shown in the screen below. This is not required for the workshop, but it is a suggested best practice to ensure consistency and reproducibility of the experimentations.

	<img src="images/create_bucket_window_2.png" alt="create bucket window 2" width="500px" />

	Press **Next** and then **Next** again leaving the settings as they are in the following screen.
7. Finally, click **Create Bucket** in the Review page.


## Create a managed Jupyter Notebook instance
We are now ready to create an Amazon SageMaker managed Jupyter notebook instance.
An **Amazon SageMaker notebook instance** is a fully managed ML compute instance running the <a href="http://jupyter.org/">**Jupyter Notebook**</a> application. Amazon SageMaker manages creating the instance and related resources. 

1. In the AWS Management Console, click on Services, type “SageMaker” and press enter.
	
	<img src="images/search_sagemaker.png" alt="Search SageMaker" width="700px" />
2. You’ll be placed in the Amazon SageMaker dashboard. Click on **Notebook instances** either in the landing page or in the left menu.
	
	<img src="images/sagemaker_dashboard.png" alt="SageMaker dashboard" width="700px" />
	
3. Once in the Notebook instances screen, click on the top-righ button **Create notebook instance**.

	<img src="images/notebook_instances_screen.png" alt="Notebook Instances screen" width="700px" />
 
4. In the **Create notebook instance** screen

	<img src="images/create_notebook_instance_screen.png" alt="Create Notebook Instance screen" width="700px" />

	1. Give the Notebook Instance a name like _endtoendml-nb-**[your-initials]**_

	2. Choose **ml.t2.medium** as **Notebook instance type**
	3. In the **IAM role** dropdown list you need to select an AWS IAM Role that is configured with security policies allowing access to Amazon SageMaker, AWS Glue and Amazon S3. You have two options here:

		3.1. If you are using an AWS Account that has been provided by an AWS instructor, a IAM role might have been previously configured for you. In such case, you just need to select the role from the dropdown (check with AWS instructor). Generally the role will be named like _AmazonSageMaker-ExecutionRole-[some-timestamp]_.
		
		3.2. If you are using your own AWS Account choose **Create a new role** in the **IAM role** dropdown list. Then, choose **Specific S3 buckets** in the **Create an IAM role** window and input the name of the bucket that you have created in the previous section. Finally, click on **Create role**.

		> Since this role needs extra policies for additional permissions, we will complete its configuration in the next section.
	
		<img src="images/sagemaker_create_role_window.png" alt="Create IAM Role window" width="600px" />

	4. Keep **No VPC** selected in the **VPC** dropdown list
	5. Keep **No configuration** selected in the **Lifecycle configuration** dropdown list
	6. Keep **No Custom Encryption** selected in the **Encryption key** dropdown list
	7. Finally, click on **Create notebook instance**

4. You will be redirected to the **Notebook instances** screen and you will see a new notebook instance in _Pending_ state.

	<img src="images/notebook_instances_pending.png" alt="Notebook instances pending" width="700px" />
	
	Wait until the notebook instance is status is _In Service_ and then click on the **Open** button to be redirected to Jupyter.

	<img src="images/notebook_instances_in_service.png" alt="Notebook instances in service" width="700px" />
	
	<img src="images/jupyter_screen.png" alt="Jupyter screen" width="700px" />

### Grant additional permissions to the IAM Role
If in the step 3.2 of the previous section you created a new IAM Role, we have to grant the role additional permissions to access additional AWS services that will be used in this workshop.

More specifically, we will need to grant:

1. ssssa
2. assaassa
3. sdsd

sasasasa.

## Download workshop code to the notebook instance

All the code of this workshop is pre-implemented and available for download from GitHub.

As a consequence, in this section we will clone the GitHub repository into the Amazon SageMaker notebook instance and access the Jupyter Notebooks to build our model.

1. Click on **New > Terminal** in the right-hand side of the Jupyter interface
	
	<img src="images/jupyter_new_terminal.png" alt="Jupyter New Terminal screen" width="700px" />

	This will open a terminal window in the Jupyter interface
	
	<img src="images/jupyter_terminal.png" alt="Jupyter Terminal screen" width="700px" />

2. Execute the following commands in the terminal

	```bash
	cd SageMaker/
	git clone https://github.com/giuseppeporcelli/end-to-end-ml-application.git
	```
3. When the clone operation completes, close the terminal window and return to the Jupyter landing page. The folder **end-to-end-ml-application** will appear automatically (if not, you can hit the **Refresh** button)

	<img src="images/jupyter_cloned_workshop_screen.png" alt="Jupyter Cloned Workshop Screen" width="700px" />
	
4. Browse to the folder **end-to-end-ml-application > 02_xxxx_xxxx** and open the file **xxxxx.ipynb** to start the data exploration and preparation step.
