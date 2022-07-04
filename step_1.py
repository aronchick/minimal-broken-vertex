import kfp
from kfp.v2.dsl import component, Artifact, Input, InputPath, Output, OutputPath, Dataset, Model
from typing import NamedTuple


def step_1_fn(
    output_context_path: OutputPath(str),
):
    import dill
    from pathlib import Path

    a = 10

    with open(Path(output_context_path).absolute(), "wb") as writer:
        dill.dump_session(filename=writer)
