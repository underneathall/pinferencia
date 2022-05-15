# Requirements

To use Pinferencia's frontend with your model, there are some requirements of  your model's predict function.

## Templates

Currently, there are mainly two major catogory of the template's inputs and outputs. More (audio and video) will be supported in the future.

### Base Templates

| Template | Input | Output |
|----------|-------|--------|
| Text to Text | Text | Text |
| Text to Image | Text | Image |
| Image to Text | Image | Text |
| Camera to Text | Image | Text |
| Image to Image | Image | Image |
| Camera to Image | Image | Image |

### Derived Templates

| Template | Input | Output |
|----------|-------|--------|
| Translation | Text | Text |
| Image Classification | Image | Text |
| Image Style Transfer | Image | Image |

## Input

1. The predict function must be able to accept a list of data as inputs.
2. For text input, the input will be a list of strings.
3. For image input, the input will be a list of strings representing the base64 encoded images.

## Output

1. The predict function must produce a list of data as outputs.
2. For text output, the output must be a list.
3. For image output, the output must be a list of strings representing the base64 encoded images.

!!! tip "Text Output"

    The frontend will try to parse the outputs into table, json or pure text.

    === "Table"

        If the output is similar to below:

        ```json
        [
            [
                {"a": 1, "b": 2},
                {"a": 3, "b": 4},
                {"a": 5, "b": 6}
            ]
        ]
        ```

        It will be displayed as a table.

    === "Text"

        If the output is similar to below:

        ```json
        [
            "Text output."
        ]
        ```

        It will be displayed as a text.

    === "JSON"

        All other format of outputs will be displayed as a JSON.
