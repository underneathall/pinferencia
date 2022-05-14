from pinferencia import Server, task


def return_text(data):
    return ["abcdefg"]


def return_json(data):
    return [{"a": 1, "b": 2}]


def return_table(data):
    return [[{"a": 1, "b": 2}, {"a": 3, "b": 4}]]


def return_invalid_table(data):
    return [[{"a": 1, "b": 2}, {"a": 3, "b": 4}, 1, 2]]


def return_image(data):
    return [
        "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+uhfwXqy2Ph25VYnPiB3SzhUkPlXCfNkAAEsCCCeOeKx9RsLjStUu9Ou1C3NpM8Eqg5AdSVIz35FVqK9xl0HXhb/C20sdMubjTLMQXs11AhkRXmmDsCwzgAYPpz+XI/GrSLrTfiVqNzPapbw3xE8AWQNvUAKXOOmWVjg+teeUV2fgXxd4hsPE2hWEGuX8Vh9uhja3Fw3lbGcBhtzjGCad8XI7iL4p68twHDGcMm45+QqCuPbBFcVRRU97fXepXb3d9dT3VzJjfNPIXdsAAZY8nAAH4VBX/9k="  # noqa
    ]


service = Server()
service.register(
    model_name="invalid-task-model",
    model=return_text,
    metadata={"task": "invalid"},
)
service.register(
    model_name="return-text-model",
    model=return_text,
    version_name="v1",
    metadata={"task": task.TEXT_TO_TEXT},
)
service.register(
    model_name="return-image-model",
    model=return_image,
    version_name="v1",
    metadata={"task": task.TEXT_TO_IMAGE},
)
service.register(
    model_name="return-json-model",
    model=return_json,
    version_name="v1",
    metadata={"task": task.TEXT_TO_TEXT},
)
service.register(
    model_name="return-table-model",
    model=return_table,
    version_name="v1",
    metadata={"task": task.TEXT_TO_TEXT},
)
service.register(
    model_name="return-invalid-table-model",
    model=return_invalid_table,
    version_name="v1",
    metadata={"task": task.TEXT_TO_TEXT},
)
