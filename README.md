# saddle

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- saddle - Source code for the application's Lambda function.
- hello_world - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Development

### Aim
The aim of this project is to create a serverless application that can be used to manage a catalogue_saddle. The application will allow users to create, read, update and delete saddles from a database.
##### Note: You should have a user IAM role with the necessary permissions.

### User Stories
1. As a user, I want to be able to create a new saddle in the database.
2. As a user, I want to be able to read all saddles in the database.
3. As a user, I want to be able to read a single saddle in the database.
4. As a user, I want to be able to update a single saddle in the database.

### Database Schema
The database will have the following schema:
- id: int
- brand: string
- model: string
- material: string
- size: string

### Routes
The application will have the following routes:
- POST /saddle
- GET /saddle
- GET /saddle/{id}
- PUT /saddle/{id}
- DELETE /saddle/{id}
- GET /health

### Technologies
The application will use the following technologies:
- Python
- AWS Lambda
- AWS API Gateway
- PostgreSQL

### Dependencies
The application will use the following dependencies:
- psycopg2
- pytest
- pytest-mock
- pytest-cov
- requests
- boto3

### steps 
1. Create a new project using the AWS SAM CLI
2. Create a directory called `saddle`
3. Use py commands to create a new virtual environment

```bash
python -m venv venv
```

4. Activate the virtual environment

```bash
.\venv\Scripts\activate
```

5. Create a file with freeze requirements.txt in the saddle directory and add the following dependencies

```bash
cd .\saddle
pip freeze > requirements.txt
```

6 Write the dependencies in the requirements.txt file
```bash
psycopg2
pyscopg2-binary
```

7. Install requirements.txt
```bash
pip install -r requirements.txt

```
- There a problem with the psycopg2 library, so we will use the psycopg2-binary library instead.



## Deploy application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. 


To build and deploy your application for the first time, run the following in your shell:

```bash
sam build 
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.


The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        saddle:
          Type: Api
          Properties:
            Path: /saddle_get_all
            Method: get
```
.

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
saddle_get_all$ pip install -r tests/requirements.txt --user
# unit test
saddle_get_all$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
saddle_get_all$ AWS_SAM_STACK_NAME="saddle" python -m pytest tests/integration -v
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
sam delete --stack-name "saddle"
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
