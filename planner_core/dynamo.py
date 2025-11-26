import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "FarmPlans"
table = dynamodb.Table(TABLE_NAME)


# -------------------------------
# SAVE A PLAN
# -------------------------------
def save_plan(plots, username):
    plan_id = str(uuid.uuid4())
    item = {
        "plan_id": plan_id,
        "username": username,
        "created_at": datetime.utcnow().isoformat(),
        "plots": plots,
    }

    table.put_item(Item=item)
    print("Saved to DynamoDB:", item)
    return plan_id


# -------------------------------
# GET ALL PLANS
# -------------------------------
def get_all_plans():
    response = table.scan()
    return response.get("Items", [])
