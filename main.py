import json
from argparse import ArgumentParser
from base64 import b64decode
from dataclasses import asdict
from pathlib import Path
from typing import Any, Optional

import onnx
import onnx.onnx_cpp2py_export.defs as C
from google.protobuf.json_format import MessageToDict

from models import Operator

"""
JSON schema for operator:

OperatorList := List[Operator]

Operator :=
{
    "name": str,
    "domain": str,
    "support_level": "COMMON" | "EXPERIMENTAL",
    "doc": str,
    "since_version": int,
    "deprecated": bool,
    "min_input": int,
    "max_input": int | "infty",
    "min_output": int,
    "max_output": int | "infty",
    "attributes": Dict[str, Attribute]
    "inputs": List[FormalParameter],
    "outputs": List[FormalParameter],
    "type_constraints": List[TypeConstraintParam],
}

Attribute := 
{
    "name": str,
    "description": str,
    "type": AttrType,
    "default_value": AttributeProto, // comes from operator.proto3
    "required": bool,
}

AttrType :=
    "FLOAT" |
    "INT" |
    "STRING" |
    "TENSOR" |
    "GRAPH" |
    "SPARSE_TENSOR" |
    "TYPE_PROTO" |
    "FLOATS" |
    "INTS" |
    "STRINGS" |
    "TENSORS" |
    "GRAPHS" |
    "SPARSE_TENSORS" |
    "TYPE_PROTOS"

FormalParameter :=
{
    "name": str,
    "types": List[str],
    "typeStr": str,
    "description": str,
    "option": "Single" | "Optional" | "Variadic",
    "isHomogeneous": bool,
    "differentiationCategory": "Unknown" | "Differentiable" | "NonDifferentiable",
}

TypeConstraintParam :=
{
    "type_param_str": str,
    "description": str,
    "allowed_type_strs": List[str],
}

"""

parser = ArgumentParser(
    prog="onnx-operators-json",
    description="""
        Transform the ONNX standard operators into JSON formats.
    """,
)
parser.add_argument(
    "-l", "--latest", action="store_true", help="only transform the latest operators"
)
output_group = parser.add_mutually_exclusive_group()
output_group.add_argument(
    "-d",
    "--output-dir",
    metavar="DIR",
    dest="output_dir",
    help="specify the output dir, and filename is `${ONNX_VERSION}.json`. Default is `op_jsons/`.",
)
output_group.add_argument(
    "-f",
    "--output-file",
    metavar="FILE",
    dest="output_file",
    help="specify the output file",
)
indent_group = parser.add_mutually_exclusive_group()
indent_group.add_argument(
    "--indent", help="specify the indent of the output json file. Default is 4.", default=4, type=int
)
indent_group.add_argument(
    "--no-indent",
    dest="no_indent",
    action="store_true",
    help="prohibit the indentation",
)


class OpJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, onnx.AttributeProto):
            d = MessageToDict(o)
            if d.get("type", None) is not None:
                if d["type"] == "STRING":
                    d["s"] = self.base64_decode(d["s"])
                elif d["type"] == "STRINGS":
                    d["strings"] = list(map(self.base64_decode, d["strings"]))
            return d
        return super().default(o)

    @classmethod
    def base64_decode(cls, s: str):
        return b64decode(s.encode("ascii")).decode("utf8")


def generate_json(
    output_dir: str = "op_jsons/",
    output_file: Optional[str] = None,
    only_latest: bool = False,
    json_indent: Optional[int] = 4,
):
    # determine the output file
    if output_file is not None:
        file = Path(output_file)
    else:
        file = Path(output_dir).joinpath(f"{onnx.__version__}.json")
    # generator dict
    ret = list()
    schemas = C.get_all_schemas() if only_latest else C.get_all_schemas_with_history()
    for schema in schemas:
        op = asdict(Operator().from_obj(schema))
        ret.append(op)
    # sort
    ret.sort(key=lambda x: (x["name"], x["since_version"]))
    # save file
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("w", encoding="utf8") as fp:
        json.dump(ret, fp, cls=OpJSONEncoder, indent=json_indent)


if __name__ == "__main__":
    args = parser.parse_args()
    generate_json(
        output_dir=args.output_dir,
        output_file=args.output_file,
        only_latest=args.latest,
        json_indent=None if args.no_indent else args.indent,
    )
    pass
