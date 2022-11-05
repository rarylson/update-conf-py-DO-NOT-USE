""" Update build status information from CodeBuild EventBridge events
"""

import os

import boto3


def lambda_handler(event, context):
    if (event["detail-type"] == "CodeBuild Build State Change"
            and event["detail"]["build-status"] in ["SUCCEEDED", "FAILED"]):
        set_build_status(
            event["detail"]["project-name"],
            event["detail"]["build-status"]
        )


def set_build_status(build_project, build_status):
    dynamodb_client = boto3.client("dynamodb")
    
    dynamodb_client.put_item(
        TableName=os.environ["DYNAMODB_TABLE"],
        Item={
            "build_project": {"S": build_project},
            "build_status": {"S": build_status}
        }
    )

