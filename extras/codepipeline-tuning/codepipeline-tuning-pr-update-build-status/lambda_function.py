""" Update CodeBuild build status on the CodeCommit pull request
"""

import os

import boto3


def lambda_handler(event, context):
    codebuild_client = boto3.client("codebuild")
    
    event_detail = event["detail"]
    env_vars = event_detail["additional-information"]["environment"]["environment-variables"]
    # Recover pull request parameters (if they exist)
    pull_request_id = None
    for item in env_vars:
        if item["name"] == "EXTRA_PULL_REQUEST_ID":
            pull_request_id = item["value"]
        elif item["name"] == "EXTRA_PULL_REQUEST_REPO_NAME":
            repo_name = item["value"]
        elif item["name"] == "EXTRA_PULL_REQUEST_DESTINATION_COMMIT":
            destination_commit = item["value"]
        elif item["name"] == "EXTRA_PULL_REQUEST_SOURCE_COMMIT":
            source_commit = item["value"]
    # Check if build was started in response to a CodeCommit pull request
    if not pull_request_id:
        return
    # Post status update comment on pull request
    post_status_update_comment_on_pull_request(
            pull_request_id, repo_name, destination_commit, source_commit, event_detail)
    

def post_status_update_comment_on_pull_request(
        pull_request_id, repo_name, destination_commit, source_commit, event_detail):
    codecommit_client = boto3.client("codecommit")

    codecommit_client.post_comment_for_pull_request(
        pullRequestId=pull_request_id,
        repositoryName=repo_name,
        beforeCommitId=destination_commit,
        afterCommitId=source_commit,
        content=status_update_comment_pretty(event_detail)
    )


def status_update_comment_pretty(event_detail):
    url_template = ("https://{0}.console.aws.amazon.com/codesuite/codebuild/projects/{1}/build/"
        "{2}?region={0}")

    build_id = event_detail["build-id"].split("/")[-1]
    url = url_template.format(os.environ["AWS_REGION"], event_detail["project-name"], build_id)
    build_number_str = ""
    if "build-number" in event_detail["additional-information"]:
        build_number_str = " (#{})".format(
                int(event_detail["additional-information"]["build-number"]))

    return "Build [{}{}]({}) update: {}".format(
            build_id, build_number_str, url, get_simple_badge(event_detail["build-status"]))


def get_simple_badge(build_status):
    # Although not documented, 'PENDING' seems to be used for builds started from batches.
    if build_status in ["PENDING", "IN_PROGRESS", "STOPPED"]:
        return "⚪ {}".format(build_status)
    elif build_status == "SUCCEEDED":
        return "🟢 {}".format(build_status)
    elif build_status == "FAILED":
        return "🔴 {}".format(build_status)
    else:
        raise RuntimeError("Unexpected build status: {}".format(event_detail["build-status"]))


# Just for reference - Do not use
# Currently CodeCommit doesn't seem to be rendering images (besides the project badge uuid URL).
# See: https://github.com/aws-samples/aws-codecommit-pull-request-aws-codebuild/issues/3
def get_shields_io_badge(build_status):
    badge_template = "https://img.shields.io/badge/build-{0}-{1}.svg?logo=amazonaws"

    # Although not documented, 'PENDING' seems to be used for builds started from batches.
    if build_status in ["PENDING", "IN_PROGRESS", "STOPPED"]:
        badge = badge_template.format(build_status.lower().replace("_", " "), "inactive")
    elif build_status == "SUCCEEDED":
        badge = badge_template.format("passing", "success")
    elif build_status == "FAILED":
        badge = badge_template.format("failing", "critical")
    else:
        raise RuntimeError("Unexpected build status: {}".format(event_detail["build-status"]))

    return "![]({})".format(badge)

