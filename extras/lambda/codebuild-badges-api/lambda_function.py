""" Return CodeBuild build status information for API integration with
shields.io
"""

import json
import os

import boto3


def lambda_handler(event, context):
    if event["requestContext"]["http"]["method"] == "GET":
        build_project = event["requestContext"]["http"]["path"].split("/")[1]
        return {
            'statusCode': 200,
            'body': get_shields_io_json(build_project)
        }
    else:
        return {
            'statusCode': 405
        }


def get_shields_io_json(build_project):
    dynamodb_client = boto3.client("dynamodb")

    # Get build_status
    response = dynamodb_client.get_item(
        TableName=os.environ["DYNAMODB_TABLE"],
        Key={"build_project": {"S": build_project}}
    )
    try:
        build_status = response["Item"]["build_status"]["S"]
    except KeyError:
        build_status = None

    # Map build status to message/color
    if build_status == "SUCCEEDED":
        message = "passing"
        color = "success"
    elif build_status == "FAILED":
        message = "failing"
        color = "critical"
    else:
        message = "no status"
        color = "inactive"

    # Return JSON in the format expected by shields.io
    # See: https://shields.io/endpoint
    return json.dumps({
        "schemaVersion": 1,
        "label": build_project,
        "message": message,
        "color": color
    }, indent=4)

