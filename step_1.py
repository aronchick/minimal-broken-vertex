import kfp
from kfp.v2.dsl import component, Artifact, Input, InputPath, Output, OutputPath, Dataset, Model
from typing import NamedTuple


def step_1_fn(
    output_context_path: OutputPath(str),
):
    import dill

    a = 10

    dill.dump_session(output_context_path)
