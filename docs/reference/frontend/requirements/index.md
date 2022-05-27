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

Based on the schema of the request, frontend end may parse the input into a list or simply a single string.

!!! info "Define Schema"
    About how to define schema of request and response, please visit [How to Define the Schema of Request and Response of Your Service?](../../../how-to-guides/schema/)

If you define your schema request as a list, for example, List[str], or simply list:

1. The predict function must be able to accept a list of data as inputs.
2. For text input, the input will be a list of strings.
3. For image input, the input will be a list of strings representing the base64 encoded images.

Otherwise,

1. The predict function must be able to accept a single data as the input.
2. For text input, the input will be a single string.
3. For image input, the input will be a single string representing the base64 encoded image.

## Output

If you define your schema response as a list, for example, List[str], or simply list:

1. The predict function must produce a list of data as outputs.
2. For text output, the output must be a list.
3. For image output, the output must be a list of strings representing the base64 encoded images.

Otherwise,

1. The predict function must produce a single data as the output.
2. For text output, the output should be a single string.
3. For image output, the output should be a single string representing the base64 encoded image.

!!! tip "Text Output"

    The frontend will try to parse the text outputs into a table, a json or pure texts.

    === "Table"

        If the output is similar to below:

        ```json title="If the schema of the response is a list"
        [
            [
                {"a": 1, "b": 2},
                {"a": 3, "b": 4},
                {"a": 5, "b": 6}
            ]
        ]
        ```

        or


        ```json title="If the schema of the response is a not list"
        [
            {"a": 1, "b": 2},
            {"a": 3, "b": 4},
            {"a": 5, "b": 6}
        ]
        ```

        It will be displayed as a table.

    === "Text"

        If the output is similar to below:

        ```json title="If the schema of the response is a list"
        [
            "Text output."
        ]
        ```
        or

        ```json title="If the schema of the response is a not list"
        "Text output."
        ```

        It will be displayed as a text.

    === "JSON"

        All other format of outputs will be displayed as a JSON.

        For example,

        ```json
        [
            [
                {"a": 1, "b": 2},
                1,
                "a"
            ]
        ]
        ```

        or 

        ```json
        {
            "a": 1,
            "b": 2
        }
        ```
