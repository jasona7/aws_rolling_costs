
### **1. Overview**

This document provides detailed information on the Daily Charges Lambda function responsible for retrieving and sending daily AWS charges. The function queries the AWS Cost Explorer API to obtain cost and usage data for the most recent 3 days and then sends the retrieved information to an SNS topic for delivery to subscribers.

### **2. Prerequisites**

- AWS account with necessary permissions for Lambda, AWS Cost Explorer, and SNS.
- AWS CLI installed and configured with the necessary credentials.
- Python 3.x installed on your local machine.
- `boto3` library installed in the Python environment. Install using:
  ```bash
  pip install boto3
  ```

### **3. Installation & Deployment**

**Step 1:** Navigate to the root directory of the project.

**Step 2:** Package the Lambda function:

```bash
zip -r9 function_package.zip lambda_function/
```

**Step 3:** Deploy the Lambda function using the AWS CLI:

```bash
aws lambda create-function --function-name DailyChargesFunction \
--runtime python3.x --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_IAM_ROLE \
--handler lambda_function.costs.lambda_handler \
--zip-file fileb://function_package.zip
```
Replace `YOUR_ACCOUNT_ID` with your AWS account ID and `YOUR_IAM_ROLE` with the IAM role that the Lambda function will assume and specify Python release.

### **4. Usage**

The function is designed to run daily. It can be triggered manually or set up with a CloudWatch Events rule for automatic execution.

**Manual Execution:**
Use the AWS CLI to manually invoke the function:

```bash
aws lambda invoke --function-name DailyChargesFunction --cli-binary-format raw-in-base64-out --payload fileb://payload.json outputfile.txt
```

`payload.json` can be an empty JSON file as the function does not rely on specific input parameters.

**Automatic Execution:**
Set up a CloudWatch Events rule to trigger the function daily. In the AWS Management Console:
1. Navigate to AWS CloudWatch/Events.
2. Choose "Rules" from the left panel and click "Create Rule".
3. For "Event Source", choose "Schedule".
4. Set the desired frequency (e.g., daily at a specific time).
5. Add the Lambda function as the target.
6. Save the rule.

### **5. Maintenance & Monitoring**

- Regularly monitor the execution logs in CloudWatch to check for any issues or errors.
- Update the IAM role if additional AWS services or permissions are required.
- Periodically review the SNS topic's subscribers to ensure the correct recipients are being notified.


## **Unit Test Documentation for AWS Lambda Function: Daily AWS Charges**

### **1. Overview**

This document provides a detailed explanation of the unit test implemented for the AWS Lambda function responsible for retrieving and sending daily AWS charges. The function’s code resides in the `lambda_function/costs.py` file, and the corresponding test is located in the `tests/test_costs.py` file.

### **2. Objective**

The primary aim of this unit test is to ensure that the Lambda function operates as expected, accurately interacting with the AWS Cost Explorer API and the SNS topic. The test focuses on the function’s ability to:
- Query the AWS Cost Explorer API for cost and usage data.
- Process and format the retrieved data.
- Publish a message containing the processed data to an SNS topic.

### **3. Test Details**

The test, named `test_lambda_handler`, specifically targets the `lambda_handler` function within the `costs.py` file.

**Mocking:**
- The `boto3.client` method is mocked to simulate the AWS Cost Explorer API and SNS interactions.
- AWS Cost Explorer API response is mocked to return predefined cost and usage data.
- The `send_sns_message` function is also mocked to avoid sending actual SNS notifications during testing.

**Execution:**
- The test executes the `lambda_handler` function, providing it with a mocked event and context.
- It then verifies whether the `send_sns_message` function gets called with the expected arguments.

### **4. Execution Instructions**

To execute the test, navigate to the root directory of the project where the `lambda_function` and `tests` directories reside. Run the following command:

```bash
python -m unittest tests/test_costs.py
```

### **5. Expected Results**

Upon successful execution, the test should pass without any errors or failures, ensuring that the `lambda_handler` function interacts correctly with the AWS services and processes the data as intended.

```bash
~/daily_cost_notices$ python -m unittest tests/test_costs.py
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```
---

Feel free to modify or extend this documentation as needed based on your specific requirements and coding conventions.# aws_rolling_costs
