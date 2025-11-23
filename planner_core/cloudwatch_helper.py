import boto3
import time
from botocore.exceptions import ClientError

cloudwatch = boto3.client("logs", region_name="us-east-1")

def create_log_group(group_name):
    """Create log group if it does not exist."""
    try:
        cloudwatch.create_log_group(logGroupName=group_name)
        print(f"Log group created: {group_name}")
    except cloudwatch.exceptions.ResourceAlreadyExistsException:
        print(f"Log group already exists: {group_name}")
    except ClientError as e:
        print("Error creating log group:", e)


def create_log_stream(group_name, stream_name):
    """Create log stream for a user if not exists."""
    try:
        cloudwatch.create_log_stream(
            logGroupName=group_name,
            logStreamName=stream_name
        )
        print(f"Log stream created: {stream_name}")
    except cloudwatch.exceptions.ResourceAlreadyExistsException:
        print(f"Log stream already exists: {stream_name}")
    except ClientError as e:
        print("Error creating log stream:", e)


def put_log_event(group_name, stream_name, message):
    """Insert a new log into CloudWatch."""
    try:
        # Get upload token
        response = cloudwatch.describe_log_streams(
            logGroupName=group_name,
            logStreamNamePrefix=stream_name
        )

        upload_seq = response["logStreams"][0].get("uploadSequenceToken")

        log_event = {
            "logGroupName": group_name,
            "logStreamName": stream_name,
            "logEvents": [
                {
                    "timestamp": int(time.time() * 1000),
                    "message": message
                }
            ]
        }

        if upload_seq:
            log_event["sequenceToken"] = upload_seq

        # Send to CloudWatch
        cloudwatch.put_log_events(**log_event)

        print("Log sent to CloudWatch.")

    except Exception as e:
        print("Error sending log:", e)
