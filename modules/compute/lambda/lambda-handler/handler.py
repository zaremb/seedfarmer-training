import os

import boto3
from aws_lambda_powertools import Logger

logger = Logger()


BUCKET_NAME = os.environ["BUCKET_NAME"]

s3_client = boto3.client("s3")


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    # List all objects in the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)

    # Iterate over each object in the bucket
    for obj in response.get("Contents", []):
        # Check if the object is a JSON file
        if obj["Key"].endswith(".json"):
            # Retrieve the JSON file content
            response = s3_client.get_object(Bucket=BUCKET_NAME, Key=obj["Key"])
            json_data = response["Body"].read().decode("utf-8")

            # Print the JSON file content
            logger.info(f'File: {obj["Key"]}\n{json_data}')

    return {"statusCode": 200, "body": "JSON files processed successfully"}
