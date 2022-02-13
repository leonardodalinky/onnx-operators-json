# onnx-operators-json

🤖 Auto-generate JSON definitions for standard ONNX operators.

## Prerequisite

```bash
pip install -r requirements.txt
```

## Usage

```
python main.py -h

usage: onnx-operators-json [-h] [-l] [-d DIR | -f FILE]
                           [--indent INDENT | --no-indent]

Transform the ONNX standard operators into JSON formats.

optional arguments:
  -h, --help            show this help message and exit
  -l, --latest          only transform the latest operators
  -d DIR, --output-dir DIR
                        specify the output dir, and filename is
                        `${ONNX_VERSION}.json`. Default is `op_jsons/`.
  -f FILE, --output-file FILE
                        specify the output file
  --indent INDENT       specify the indent of the output json file. Default is
                        4.
  --no-indent           prohibit the indentation
```

## JSON-schema

```python
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
    "default_value": AttributeProto, # comes from operator.proto3
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
```

Example of operators:
<details>
<summary>Operator of ConvTranspose</summary>

```json
{
    "name": "ConvTranspose",
    "domain": "",
    "support_level": "COMMON",
    "doc": "\nThe convolution transpose operator consumes an input tensor and a filter,\nand computes the output.\n\nIf the pads parameteris provided the shape of the output is calculated via the following equation:\n\n  output_shape[i] = stride[i] * (input_size[i] - 1) +output_padding[i] + ((kernel_shape[i] - 1) * dilations[i] + 1) - pads[start_i] - pads[end_i]\n\noutput_shape can also be explicitlyspecified in which case pads values are auto generated using these equations:\n\n  total_padding[i] = stride[i] * (input_size[i] - 1) +output_padding[i] + ((kernel_shape[i] - 1) * dilations[i] + 1) - output_shape[i]\n  If (auto_pads == SAME_UPPER): pads[start_i] =total_padding[i]/2; pads[end_i] = total_padding[i] - (total_padding[i]/2)\n  Else: pads[start_i] = total_padding[i] - (total_padding[i]2); pads[end_i] = (total_padding[i]/2).\n\n    ",
    "since_version": 11,
    "deprecated": false,
    "min_input": 2,
    "max_input": 3,
    "min_output": 1,
    "max_output": 1,
    "attributes": {
        "auto_pad": {
            "name": "auto_pad",
            "description": "auto_pad must be either NOTSET, SAME_UPPER, SAME_LOWER or VALID. Where default value is NOTSET, which meansexplicit padding is used. SAME_UPPER or SAME_LOWER mean pad the input so that `output_shape[i] = input_shape[i] * strides[i]`for each axis `i`. The padding is split between the two sides equally or almost equally (depending on whether it is even or odd. In case the padding is an odd number, the extra padding is added at the end for SAME_UPPER and at the beginning forSAME_LOWER.",
            "type": "STRING",
            "default_value": {
                "name": "auto_pad",
                "s": "NOTSET",
                "type": "STRING"
            },
            "required": false
        },
        "dilations": {
            "name": "dilations",
            "description": "dilation value along each spatial axis of the filter. If not present, the dilation defaults to 1 along eachspatial axis.",
            "type": "INTS",
            "default_value": {},
            "required": false
        },
        "group": {
            "name": "group",
            "description": "number of groups input channels and output channels are divided into.",
            "type": "INT",
            "default_value": {
                "name": "group",
                "i": "1",
                "type": "INT"
            },
            "required": false
        },
        "kernel_shape": {
            "name": "kernel_shape",
            "description": "The shape of the convolution kernel. If not present, should be inferred from input W.",
            "type": "INTS",
            "default_value": {},
            "required": false
        },
        "output_padding": {
            "name": "output_padding",
            "description": "Additional elements added to the side with higher coordinate indices in the output. Each padding value in\"output_padding\" must be less than the corresponding stride/dilation dimension. By default, this attribute is a zero vector.Note that this attribute doesn't directly affect the computed output values. It only controls the selection of the computedvalues, so changing this attribute only adds or removes output elements. If \"output_shape\" is explicitly provided,\"output_padding\" does not contribute additional size to \"output_shape\" but participates in the computation of the neededpadding amount. This is also called adjs or adjustment in some frameworks.",
            "type": "INTS",
            "default_value": {},
            "required": false
        },
        "output_shape": {
            "name": "output_shape",
            "description": "The shape of the output can be explicitly set which will cause pads values to be auto generated. Ifoutput_shape is specified pads values are ignored. See doc for details for equations to generate pads",
            "type": "INTS",
            "default_value": {},
            "required": false
        },
        "pads": {
            "name": "pads",
            "description": "Padding for the beginning and ending along each spatial axis, it can take any value greater than or equal to 0.The value represent the number of pixels added to the beginning and end part of the corresponding axis. `pads` format should beas follow [x1_begin, x2_begin...x1_end, x2_end,...], where xi_begin the number of pixels added at the beginning of axis `i` andxi_end, the number of pixels added at the end of axis `i`. This attribute cannot be used simultaneously with auto_padattribute. If not present, the padding defaults to 0 along start and end of each spatial axis.",
            "type": "INTS",
            "default_value": {},
            "required": false
        },
        "strides": {
            "name": "strides",
            "description": "Stride along each spatial axis. If not present, the stride defaults to 1 along each spatial axis.",
            "type": "INTS",
            "default_value": {},
            "required": false
        }
    },
    "inputs": [
        {
            "name": "X",
            "types": [
                "tensor(double)",
                "tensor(float)",
                "tensor(float16)"
            ],
            "typeStr": "T",
            "description": "Input data tensor from previous layer; has size (N x C x H x W), where N is the batch size, C is the number ofchannels, and H and W are the height and width. Note that this is for the 2D image. Otherwise the size is (N x C x D1 x D2 ...x Dn)",
            "option": "Single",
            "isHomogeneous": true,
            "differentiationCategory": "Differentiable"
        },
        {
            "name": "W",
            "types": [
                "tensor(double)",
                "tensor(float)",
                "tensor(float16)"
            ],
            "typeStr": "T",
            "description": "The weight tensor that will be used in the convolutions; has size (C x M/group x kH x kW), where C is thenumber of channels, and kH and kW are the height and width of the kernel, and M is the number of feature maps. For more than 2dimensions, the weight shape will be (C x M/group x k1 x k2 x ... x kn), where (k1 x k2 x ... x kn) is the dimension of thekernel. The number of channels in the output should be equal to W.shape[1] * group (assuming zero based indices of the shapearray)",
            "option": "Single",
            "isHomogeneous": true,
            "differentiationCategory": "Differentiable"
        },
        {
            "name": "B",
            "types": [
                "tensor(double)",
                "tensor(float)",
                "tensor(float16)"
            ],
            "typeStr": "T",
            "description": "Optional 1D bias to be added to the convolution, has size of M.",
            "option": "Optional",
            "isHomogeneous": true,
            "differentiationCategory": "Differentiable"
        }
    ],
    "outputs": [
        {
            "name": "Y",
            "types": [
                "tensor(double)",
                "tensor(float)",
                "tensor(float16)"
            ],
            "typeStr": "T",
            "description": "Output data tensor that contains the result of the convolution. The output dimensions are functions of thekernel size, stride size, pad lengths and group count. The number of channels in the output should be equal to W.shape[1] *group (assuming zero based indices of the shape array)",
            "option": "Single",
            "isHomogeneous": true,
            "differentiationCategory": "Differentiable"
        }
    ],
    "type_constraints": [
        {
            "type_param_str": "T",
            "description": "Constrain input and output types to float tensors.",
            "allowed_type_strs": [
                "tensor(float16)",
                "tensor(float)",
                "tensor(double)"
            ]
        }
    ]
}
```
</details>

## Contributing

Feel free to make any issues or PRs!
