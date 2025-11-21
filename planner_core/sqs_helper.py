import boto3
import json

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/675834675118/FarmPlanQueue"

def send_plan_to_queue(plan_id, plots, username):
    """
    Send a message to SQS whenever a plan is created.
    """
    sqs = boto3.client("sqs", region_name="us-east-1")

    message = {
        "plan_id": plan_id,
        "username": username,
        "plots": plots
    }

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )

    print("SQS message sent:", message)
