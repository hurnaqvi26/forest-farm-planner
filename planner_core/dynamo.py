import boto3
import uuid
import datetime
from botocore.exceptions import ClientError

TABLE_NAME = "FarmPlans"   # DynamoDB table name


def get_table():
    """Return DynamoDB table resource."""
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    return dynamodb.Table(TABLE_NAME)


def save_plan(plots, username):
    """
    Save farm plan into DynamoDB.
    """
    plan_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()

    item = {
        "plan_id": plan_id,
        "username": username,
        "created_at": timestamp,
        "plots": plots
    }

    try:
        table = get_table()
        table.put_item(Item=item)
        print("Saved to DynamoDB:", item)

    except ClientError as e:
        print("DynamoDB Error:", e)

    return plan_id
