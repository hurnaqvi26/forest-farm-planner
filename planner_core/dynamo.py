import boto3
import uuid
from datetime import datetime

# Always specify region
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("FarmPlans")


def save_plan(plots, username, area="0", date=None):
    """
    Save a farm plan to DynamoDB.
    🔥 ALWAYS generates a unique plan_id.
    🔥 ENSURES all required fields exist.
    """

    # Always generate a plan_id
    plan_id = str(uuid.uuid4())

    # Default date
    if date is None:
        date = datetime.utcnow().isoformat()

    # Validate plots
    if not isinstance(plots, list):
        plots = []

    # Final item
    item = {
        "plan_id": plan_id,             # REQUIRED PARTITION KEY
        "username": username,
        "area": str(area),
        "date": date,
        "plots": plots,
        "created_at": datetime.utcnow().isoformat(),
    }

    # Save
    table.put_item(Item=item)

    return plan_id


def get_all_plans():
    """
    Return all plans from DynamoDB.
    """
    response = table.scan()
    return response.get("Items", [])
