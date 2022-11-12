""" Return CodeBuild build status information for API integration with
shields.io

It works standalone (with Lambda HTTP endpoints) or via integration with
API Gateway.
"""

import json
import os

import boto3
import requests


# Constants
CODEBUILD_DEFAULT_BRANCH = "main"
DEFAULT_LABEL = "build"
CODEBUILD_BADGE_PATH = "/badges"


def lambda_handler(event, context):
    # Validate requests from Lambda HTTPS endpoint
    if "http" in event["requestContext"]:
        if event["requestContext"]["http"]["method"] != "GET":
            return { "statusCode": 405 }
        if event["requestContext"]["http"]["path"] != "/build-status":
            return { "statusCode": 404 }
        if not "uuid" in event["queryStringParameters"]:
            return { 
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Missing required request parameters: [uuid]"
                })
            }
    # Get parameters for Lambda HTTPS endpoint or API Gateway 
    # integration
    uuid = event["queryStringParameters"]["uuid"]
    branch = event["queryStringParameters"].get("branch", CODEBUILD_DEFAULT_BRANCH)
    tag = event["queryStringParameters"].get("tag", None)
    label = event["queryStringParameters"].get("label", DEFAULT_LABEL)

    return {
        "statusCode": 200,
        "body": get_shields_io_json(uuid, branch, tag, label)
    }


def get_shields_io_json(uuid, branch=None, tag=None, label=DEFAULT_LABEL):
    dynamodb_client = boto3.client("dynamodb")
    codebuild_client = boto3.client("codebuild")

    # Set default branch if necessary
    if not (branch or tag):
        branch = CODEBUILD_DEFAULT_BRANCH

    # Check if uuid exist (from cache)
    try:
        dynamodb_client.get_item(
            TableName=os.environ["DYNAMODB_TABLE"],
            Key={"uuid": {"S": uuid}}
        )["Item"]
        uuid_exists = True
    except KeyError:
        uuid_exists = False

    # Get build status
    build_status = "unknown"
    if uuid_exists:
        url = "{}{}".format(codebuild_client.meta.endpoint_url, CODEBUILD_BADGE_PATH)
        # Send request to CodeBuild badge endpoint
        params = { "uuid": uuid }
        if branch:
            params["branch"] = branch
        if tag:
            params["tag"] = tag
        response = requests.get(url, params=params, allow_redirects=False)
        # Process response
        if not response.is_redirect:
            raise RuntimeError("Unexpected status code: {}".format(response.status_code))
        location = response.headers["Location"]
        build_status = location.split("/")[-1].split(".")[0]

    # Map build status to message/color
    if build_status == "passing":
        color = "success"
    elif build_status == "failing":
        color = "critical"
    elif build_status == "unknown":
        build_status = "no status"
        color = "inactive"
    else:
        raise RuntimeError("Not expected `build_status`: {}".format(build_status))
    
    # Return JSON in the format expected by shields.io
    # See: https://shields.io/endpoint
    return json.dumps({
        "schemaVersion": 1,
        "label": label,
        "message": build_status,
        "color": color
    }, indent=4)

