""" Update badge uuid cache
"""

import os
import time
from urllib.parse import parse_qs, urlparse

import boto3


# Contants
UUID_CACHE_TTL = 3600


def lambda_handler(event, context):
    update_uuid_cache()


def update_uuid_cache():
    codebuild_client = boto3.client("codebuild") 
    dynamodb_client = boto3.client("dynamodb")

    # Get current uuids
    uuids = []
    project_names = codebuild_client.list_projects()["projects"]
    for project in codebuild_client.batch_get_projects(names=project_names)["projects"]:
        if project["badge"]["badgeEnabled"]:
            uuid = parse_qs(urlparse(project["badge"]["badgeRequestUrl"]).query)["uuid"][0]
            uuids.append(uuid)

    # Update cache
    for uuid in uuids:
        dynamodb_client.put_item(
            TableName=os.environ["DYNAMODB_TABLE"],
            Item={
                "uuid": {"S": uuid},
                # Set a TTL so disabled build badges or deleted build projects will eventually
                # have their uuids deleted.
                "ttl": {"N": str(int(time.time()) + UUID_CACHE_TTL)}
            }
        )

