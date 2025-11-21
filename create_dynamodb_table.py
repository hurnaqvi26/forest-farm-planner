import boto3

dynamodb = boto3.client("dynamodb", region_name="us-east-1")

table_name = "FarmPlans"

try:
    response = dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "plan_id", "AttributeType": "S"}
        ],
        KeySchema=[
            {"AttributeName": "plan_id", "KeyType": "HASH"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    print("Table creation started...")
    print(response)

except dynamodb.exceptions.ResourceInUseException:
    print("Table already exists.")
