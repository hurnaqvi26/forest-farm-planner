import boto3
import uuid
import datetime
from botocore.exceptions import ClientError

# ----------------------------------------------------------------
# SETTINGS
# ----------------------------------------------------------------
TABLE_NAME = "FarmPlans"


def get_dynamo_table():
    """
    Returns a DynamoDB Table resource.
    (Safe to call even if AWS is deactivated — it will only fail
     if you actually call table.put_item())
    """
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    return dynamodb.Table(TABLE_NAME)


def save_plan(plots, username):
    """
    Saves a farm plan to DynamoDB.
    Returns plan_id.
    """

    plan_id = str(uuid.uuid4())
    timestamp = datetime.datetime.utcnow().isoformat()

    item = {
        "plan_id": plan_id,
        "username": username,
        "created_at": timestamp,
        "plots": plots,
    }

    try:
        table = get_dynamo_table()
        table.put_item(Item=item)
        print("Saved plan:", item)

    except ClientError as e:
        print("DynamoDB Error:", e)
        # still return plan_id even if AWS is down
        # so your project continues working
        pass

    return plan_id
