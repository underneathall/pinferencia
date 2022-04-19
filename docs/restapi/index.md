# REST API

**Pinferencia** has two built-in API sets:

=== "Default API"

    ```python
    from pinferencia import Server

    service = Server()

    # or
    service = Server(api="default")
    ```


=== "Kserve API"

    ```python
    from pinferencia import Server

    service = Server(api="kserve")
    ```

!!! question "Are you using other serving tools now?"

    If you also use other model serving tools, here are the Kserve API versions the tools support:

    | Name | API |
    |------------|---------|
    | Pinferencia | Kserve V1 & V2 |
    | TF Serving | Kserve V1 |
    | TorchServe | Kserve V1 or V2 |
    | Triton | Kserve V2 |
    | KServe | Kserve V1 |

As you can see

- You can switch between **Pinferencia** and other tools with almost no code changes in client.
- If you want to use **Pinferencia** for prototyping and client building, then use other tools in production, you got it supported out of the box.
- You can use **Pinferencia** in production with other tools with the same API set.
- If you're switching from Kserve V1 to Kserve V2 and you need a server supporting both during the transition, you got **Pinferencia**.

So, no pain, just gain.