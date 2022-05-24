# How to Define the Schema of Request and Response of Your Service?

Imagine this:

Your service calculates the sum of posted data.

It requires a request body:

```json
[1, 2, 3]
```

and returns a response body:

```json
6
```

How do you let the user know what does your request and response body look like?

And what if you want to validate/parse the request/response body automatically?

In this article, we will walk throught how to define the schema of the request and response of your service in Pinferencia.

## Python 3 Type Hint

Have you heard of `type hint` in python? If not, you better check it out now at [Python Typing](https://docs.python.org/3/library/typing.html).

Since Python 3.5, Python starts to support type hint in your function definition. You can declare the type of the arguments and return.

**Pinferencia** use the type hint of your function to define the schema of your request and response. So, you don't need to learn another format, and you can just stay with python.

!!! warning "Not all type hints are supported!"
    Not all the type hints in python can be used to define the schema. The type hints need be able to be correctly represented in the json schema.

## A Dummy Service

Let's create a dummy service to show you how everything works.

```python title="dummy.py"
from pinferencia import Server

service = Server()


def dummy(data: list) -> str:
    return data


service.register(model_name="dummy", model=dummy)
```

Start the service, and visit the backend documentation page, you will find examples of the request and response:

=== "Request Example"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            "string"
        ]
    }
    ```

=== "Response Example"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": "string"
    }
    ```

Here type hint `list` of the argument of the function will be used to define the `data` field in request body. Type hint `str` of the return of the function will be used to define the `data` field in the response body.

## The Sum Service

Now let's get back to the service at the start of this article, a sum service with:

=== "Request Example"

    ```json
    [1, 2, 3]
    ```

=== "Response Example"

    ```json
    6
    ```

Let's rewrite our dummy service

=== "Python 3.6 and above"

    ```python title="dummy.py"
    from typing import List

    from pinferencia import Server

    service = Server()


    def dummy(data: List[int]) -> int:
        return data


    service.register(model_name="dummy", model=dummy)
    ```

=== "Python 3.9 and above"

    ```python title="dummy.py"
    from pinferencia import Server

    service = Server()


    def dummy(data: list[int]) -> int:
        return sum(data)


    service.register(model_name="dummy", model=dummy)
    ```

Now visit the backend documentation page, the examples will be:

=== "Request Example"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            0
        ]
    }
    ```

=== "Response Example"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": 0
    }
    ```

Besides displaying the schema, **Pinferencia** also validates and tries to parse the data into the desired types. Let's try out the API on the backend documentation page.

=== "Normal Data"

    === "Request"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": [
                1, 2, 3
            ]
        }
        ```

    === "Response"

        ```json
        {
            "id": "string",
            "model_name": "dummy",
            "model_version": "default",
            "data": 6
        }
        ```

=== "Invalid Type Data"

    Let's change one of the number in the request to string type. And the number will be converted to integer according to the schema.

    === "Request"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": [
                "1", 2, 3
            ]
        }
        ```

    === "Response"

        ```json
        {
            "id": "string",
            "model_name": "dummy",
            "model_version": "default",
            "data": 6
        }
        ```

=== "Invalid Data"

    Let's post some invalid data type, and you will receive a `422` error

    === "Request"

        ```json
        {
            "id": "string",
            "parameters": {},
            "data": 1
        }
        ```

    === "Response"

        ```json
        {
            "detail": [
                {
                "loc": [
                    "body",
                    "data"
                ],
                "msg": "value is not a valid list",
                "type": "type_error.list"
                }
            ]
        }
        ```

## Complicated Schema

It's possible to define complicated schema in Pinferencia with the help of `pydantic`.

Let's assume a service receive a persion's information:

```json title="request"
[
    {
        "name": "Will",
        "age": 23,
        "gender": "male"
    },
    {
        "name": "Elise",
        "age": 19,
        "gender": "female"
    }
]
```

and simply reply a welcome message:

```json title="response"
"Hello, Will! Hello, Elise!"
```

Let's define the service:

```python title="welcome.py"
from typing import List

from pydantic import BaseModel

from pinferencia import Server


class Person(BaseModel):
    name: str
    age: int
    gender: str


service = Server()


def welcome(persons: List[Person]) -> str:
    message = ""
    for person in persons:
        message += "Hello, " + person.name + "!"
    return message


service.register(model_name="welcome", model=welcome)
```

Now start the service and visit the backend documentation page, you will find the request and response example as below:

=== "Request Example"

    ```json
    {
        "id": "string",
        "parameters": {},
        "data": [
            {
            "name": "string",
            "age": 0,
            "gender": "string"
            }
        ]
    }
    ```

=== "Response Example"

    ```json
    {
        "id": "string",
        "model_name": "string",
        "model_version": "string",
        "parameters": {},
        "data": "string"
    }
    ```

## Mission Completed

You have learned how to define request and response schema with **Pinferencia**. You can now try out more schemas you're interested. Have fun!
