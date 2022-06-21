import kfp.v2.components
from kfp.v2.dsl import InputPath
from kubernetes.client.models import V1EnvVar
from kubernetes import client, config
from typing import NamedTuple
from base64 import b64encode
import kfp.v2.dsl as dsl
import kubernetes
import json
import kfp
from google.cloud import aiplatform
import datetime
import pprint as pp
import requests

from step_1 import step_1_fn
from step_2 import step_2_fn

step_1_comp = kfp.v2.dsl.component(
    func=step_1_fn,
    base_image="library/python:3.10-slim-buster",
    packages_to_install=[
        "dill",
    ],
)
step_2_comp = kfp.v2.dsl.component(
    func=step_2_fn,
    base_image="library/python:3.10-slim-buster",
    packages_to_install=[
        "dill",
    ],
)


@kfp.dsl.pipeline(
    pipeline_root="gs://minimal_vertex_test_bucket",
    name="minimalcompile",
)
def root():
    step_1_exec = step_1_comp()
    step_2_exec = step_2_comp(input_context_path=step_1_exec.outputs["output_context_path"])
