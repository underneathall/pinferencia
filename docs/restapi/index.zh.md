# REST API

## 概述

**Pinferencia** 有两个内置 API：

=== "默认 API"

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

!!! question "您现在正在使用其他模型服务工具吗？"

    如果您还使用其他模型服务工具，以下是这些工具支持的 Kserve API 版本：

    | 名称 | API |
    |------------|---------|
    | Pinferencia | Kserve V1 & V2 |
    | TF Serving | Kserve V1 |
    | TorchServe | Kserve V1 or V2 |
    | Triton | Kserve V2 |
    | KServe | Kserve V1 |

## 没有痛苦，只有收获

如你看到的

- 您可以在 **Pinferencia** 和其他工具之间切换，几乎无需在客户端更改代码。
- 您可以使用 **Pinferencia** 进行原型设计和客户端构建，然后在生产中使用其他工具。
- 您可以在生产环境中将 **Pinferencia** 与具有相同 API 集的其他工具一起使用。
- 如果您要从 Kserve V1 切换到 Kserve V2，并且在过渡期间需要支持这两者的服务器，那么您就可以使用 **Pinferencia**。

所以，没有痛苦，只有收获。

## 默认 API

| Path | Method | Summary |
|------|--------|---------|
| /v1/healthz | GET | 服务健康 |
| /v1/models | GET | 模型列表 |
| /v1/models/{model_name} | GET | 模型版本列表 |
| /v1/models/{model_name}/ready | GET | 模型是否可用 |
| /v1/models/{model_name}/versions/{version_name}/ready | GET | 模型版本是否可用 |
| /v1/models/{model_name}/load | POST | 加载模型 |
| /v1/models/{model_name}/versions/{version_name}/load | POST | 加载版本 |
| /v1/models/{model_name}/unload | POST | 卸载模型 |
| /v1/models/{model_name}/versions/{version_name}/unload | POST | 卸载版本 |
| /v1/models/{model_name}/predict | POST | 模型预测 |
| /v1/models/{model_name}/versions/{version_name}/predict | POST | 模型版本预测 |

## Kserve API

| Path | Method | Summary |
|------|--------|---------|
| /v1/healthz | GET | 服务健康 |
| /v1/models | GET | 模型列表 |
| /v1/models/{model_name} | GET | 模型版本列表 |
| /v1/models/{model_name}/ready | GET | 模型是否可用 |
| /v1/models/{model_name}/versions/{version_name}/ready | GET | 模型版本是否可用 |
| /v1/models/{model_name}/load | POST | 加载模型 |
| /v1/models/{model_name}/versions/{version_name}/load | POST | 加载版本 |
| /v1/models/{model_name}/unload | POST | 卸载模型 |
| /v1/models/{model_name}/versions/{version_name}/unload | POST | 卸载版本 |
| /v1/models/{model_name}/infer | POST | 模型预测 |
| /v1/models/{model_name}/versions/{version_name}/infer | POST | 模型版本预测 |
| /v2/healthz | GET | 服务健康 |
| /v2/models | GET | 模型列表 |
| /v2/models/{model_name} | GET | 模型版本列表 |
| /v2/models/{model_name}/ready | GET | 模型是否可用 |
| /v2/models/{model_name}/versions/{version_name}/ready | GET | 模型版本是否可用 |
| /v2/models/{model_name}/load | POST | 加载模型 |
| /v2/models/{model_name}/versions/{version_name}/load | POST | 加载版本 |
| /v2/models/{model_name}/unload | POST | 卸载模型 |
| /v2/models/{model_name}/versions/{version_name}/unload | POST | 卸载版本 |
| /v2/models/{model_name}/infer | POST | 模型预测 |
| /v2/models/{model_name}/versions/{version_name}/infer | POST | 模型版本预测 |