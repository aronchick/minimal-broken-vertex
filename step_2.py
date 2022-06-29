import kfp
from kfp.v2.dsl import component, Artifact, Input, InputPath, Output, OutputPath, Dataset, Model
from typing import NamedTuple


def step_2_fn(
    input_context_path: InputPath(str),
    output_context_path: OutputPath(str),
    metadata_url: str = "",
):
    from base64 import urlsafe_b64encode, urlsafe_b64decode
    import dill
    from pathlib import Path

    dill.load_session(input_context_path)

    print(f"A = {a}")

    dill.dump_session(output_context_path)


# import kfp
# from kfp.v2.dsl import component, Artifact, Input, InputPath, Output, OutputPath, Dataset, Model
# from typing import NamedTuple
# from base64 import urlsafe_b64encode, urlsafe_b64decode
# import dill
# from pathlib import Path

# def step_2_fn(
#     input_context_path: InputPath(str),
#     output_context_path: OutputPath(str),
#     metadata_url: str = ""
# ):

#     with Path(input_context_path).open("rb") as reader:
#         input_context = reader.read()
#     	  print(f"A = {input_context}")

#     dill.dump_session("{output_context_path}")
