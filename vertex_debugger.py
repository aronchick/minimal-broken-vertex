import sys
import uuid
import click
import glob
from pathlib import Path
from kfp.v2 import compiler
import importlib
import os
import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component, Output, HTML
from google.cloud import aiplatform
import dotenv
import datetime

import os


@click.group()
def main():
    """
    Debug your SAME project compiled vertex pipelines.
    """


@click.command(
    context_settings=dict(
        ignore_unknown_options=False,
        allow_extra_args=False,
    )
)
@click.option(
    "--compiled-directory",
    "compiled_directory",
    help="Directory in which your file exists",
    show_default=True,
    required=True,
)
def compile_vertex(compiled_directory: os.strerror):
    dotenv.load_dotenv()
    sys.path.append(compiled_directory)
    p = Path(compiled_directory)

    root_files = [f for f in p.glob("root_pipeline_*.py")]
    if len(root_files) < 1:
        raise ValueError(f"No root files found in {compiled_directory}")
    elif len(root_files) > 1:
        raise ValueError(f"More than one root file found in {compiled_directory}: {', '.join(root_files)}")
    else:
        root_file = root_files.pop()

    print(f"Root file: {root_file}")
    mod = root_file.stem

    root_module = importlib.import_module(mod)

    file_suffix = ".json"

    package_json_path = p / f"root{file_suffix}"

    print(f"Package path: {package_json_path}")

    package_json_path.unlink() if package_json_path.exists() else 0

    compiler.Compiler().compile(pipeline_func=root_module.root, package_path=str(package_json_path))


@click.command(
    context_settings=dict(
        ignore_unknown_options=False,
        allow_extra_args=False,
    )
)
@click.option(
    "--compiled-pipeline-path",
    "compiled_pipeline_path",
    help="The path to your compiled pipeline JSON file. It can be a local path or a Google Cloud Storage URI.",
    show_default=True,
    required=True,
)
@click.option(
    "--project-id",
    "project_id",
    help="The project that you want to run the pipeline in.",
    show_default=True,
    required=True,
)
@click.option(
    "--service-account-credentials-file",
    "service_account_credentials_file",
    help="JSON file containing credentials for the service account.",
    show_default=True,
    required=True,
)
def deploy_vertex(compiled_pipeline_path: str, project_id: str, service_account_credentials_file: str):
    dotenv.load_dotenv()
    from google.cloud import aiplatform

    project_id = os.environ.get("PROJECT_ID", project_id)
    service_account_credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", service_account_credentials_file)
    location = "northamerica-northeast1"

    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(service_account_credentials_file)

    aiplatform.init(project=project_id, location=location, credentials=credentials)

    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    BUCKET_URI = f"gs://{BUCKET_NAME}"
    PIPELINE_ROOT = f"{BUCKET_URI}/{uuid.uuid4()}/pipeline_root"

    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    job = aiplatform.PipelineJob(
        display_name="my-display-job",
        template_path=compiled_pipeline_path,
        project=project_id,
        credentials=credentials,
        location=location,
        pipeline_root=f"{PIPELINE_ROOT}",
        job_id="my-display-job-{0}".format(TIMESTAMP),
    )

    # job = aiplatform.PipelineJob(
    #     display_name="MY_DISPLAY_JOB",
    #     template_path=compiled_pipeline_path,
    #     job_id=JOB_ID,
    #     pipeline_root=PIPELINE_ROOT_PATH,
    #     parameter_values=PIPELINE_PARAMETERS,
    #     enable_caching=ENABLE_CACHING,
    #     encryption_spec_key_name=CMEK,
    #     labels=LABELS,
    #     credentials=CREDENTIALS,
    #     project=PROJECT_ID,
    #     location=LOCATION,
    # )

    job.submit(service_account=credentials.service_account_email)
    # job.submit(service_account=SERVICE_ACCOUNT, network=NETWORK)


main.add_command(compile_vertex)
main.add_command(deploy_vertex)

# https://click.palletsprojects.com/en/8.1.x/options/#values-from-environment-variables
if __name__ == "__main__":
    main(auto_envvar_prefix="SAME")
