""" Start CodeDeploy builds from CodeCommit pull request events
"""

import os

import boto3


# Constants
TAG_KEY_BUILD_PROJECT = "CodePipelineTuning/BuildProjectForPullRequest"


def lambda_handler(event, context):
    repo_name = event["detail"]["repositoryNames"][0]
    pull_request_id = event["detail"]["pullRequestId"]
    destination_commit =  event["detail"]["destinationCommit"]
    source_commit = event["detail"]["sourceCommit"]
    branch_ref = event["detail"]["sourceReference"]

    # Get repository details
    repo_details = get_repo_details(repo_name)
    # Check if feature 'build on pull request' is enabled
    if not TAG_KEY_BUILD_PROJECT in repo_details["tags"]:
        return
    # Get build project that should be used
    build_project = repo_details["tags"][TAG_KEY_BUILD_PROJECT]
    # Start build
    build_info = start_build(
            build_project, source_commit, branch_ref, pull_request_id, repo_name,
            destination_commit)
    # Post initial comment on pull request
    post_init_comment_on_pull_request(
            pull_request_id, repo_name, destination_commit, source_commit, build_info)


def get_repo_details(repo):
    codecommit_client = boto3.client("codecommit")

    repo_details = codecommit_client.get_repository(repositoryName=repo)["repositoryMetadata"]
    tags = codecommit_client.list_tags_for_resource(resourceArn=repo_details["Arn"])["tags"]
    repo_details["tags"] = tags

    return repo_details


def start_build(
        build_project, source_commit, branch_ref, pull_request_id, repo_name, destination_commit):
    codebuild_client = boto3.client("codebuild")

    build_spec = {
        "projectName": build_project,
        "sourceVersion": source_commit,
        # Disable artifacts
        "artifactsOverride": {
            "type": "NO_ARTIFACTS"
        },
        "secondaryArtifactsOverride": [],
        "environmentVariablesOverride": [
            # Source branch reference (in case the buildspec file needs it)
            # See: https://github.com/thii/aws-codebuild-extras/issues/3
            {
                "name": "EXTRA_SOURCE_REF",
                "value": branch_ref,
                "type": "PLAINTEXT"
            },
            # Pull request related vars (the Lambda function 
            # 'codepipeline-tuning-update-pull-request' will need them)
            {
                "name": "EXTRA_PULL_REQUEST_ID",
                "value": pull_request_id,
                "type": "PLAINTEXT"
            },
            {
                "name": "EXTRA_PULL_REQUEST_REPO_NAME",
                "value": repo_name,
                "type": "PLAINTEXT"
            },
            {
                "name": "EXTRA_PULL_REQUEST_SOURCE_COMMIT",
                "value": source_commit,
                "type": "PLAINTEXT"
            },
            {
                "name": "EXTRA_PULL_REQUEST_DESTINATION_COMMIT",
                "value": destination_commit,
                "type": "PLAINTEXT"
            }
        ]
    }
    project_details = codebuild_client.batch_get_projects(names=[build_project])["projects"][0]
    if "buildBatchConfig" in project_details:
        response = codebuild_client.start_build_batch(**build_spec)
        return {
            "is_batch": True,
            "build_project": build_project,
            "build_id": response["buildBatch"]["id"],
            "build_number": response["buildBatch"]["buildBatchNumber"]
        }
    else:
        response = codebuild_client.start_build(**build_spec)
        return {
            "built_type": False,
            "build_project": build_project,
            "build_id": response["build"]["id"],
            "build_number": response["build"]["buildNumber"]
        }


def post_init_comment_on_pull_request(
        pull_request_id, repo_name, destination_commit, source_commit, build_info):
    codecommit_client = boto3.client("codecommit")

    codecommit_client.post_comment_for_pull_request(
        pullRequestId=pull_request_id,
        repositoryName=repo_name,
        beforeCommitId=destination_commit,
        afterCommitId=source_commit,
        content=init_comment_pretty(build_info)
    )


def init_comment_pretty(build_info):
    codebuild_client = boto3.client("codebuild")
    url_template = ("https://{0}.console.aws.amazon.com/codesuite/codebuild/projects/{1}/{2}/{3}"
            "?region={0}")

    url = url_template.format(
            os.environ["AWS_REGION"], build_info["build_project"], 
            "batch" if build_info["is_batch"] else "build", build_info["build_id"])
    build_type_str = "Batch build" if build_info["is_batch"] else "Build"

    return "{} [{} (#{})]({}) started.".format(
            "Batch build" if build_info["is_batch"] else "Build",
            build_info["build_id"], build_info["build_number"], url)

