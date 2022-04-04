from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/models/{model_name}/ready", response_model=bool)
async def model_is_ready(request: Request, model_name: str):
    """Indicate Whether the Model is Ready for Prediction

    You need to pass the model name registered for the model in
    the URL.

    - If the API returns **ture**, it means the model is ready.
    - If the API returns **false**, it means the model is not ready.
      You need to call the **Load Model** API to load the model.
    """
    return request.app.model.repository.is_ready(model_name)


@router.get(
    "/models/{model_name}/versions/{version_name}/ready", response_model=bool
)
async def model_version_is_ready(
    request: Request,
    model_name: str,
    version_name: str,
):
    return request.app.model.repository.is_ready(model_name, version_name)


@router.post("/models/{model_name}/load", response_model=bool)
async def load_model(request: Request, model_name: str):
    return request.app.model.repository.load_model(model_name)


@router.post(
    "/models/{model_name}/versions/{version_name}/load", response_model=bool
)
async def load_version(request: Request, model_name: str, version_name: str):
    return request.app.model.repository.load_model(
        model_name, version_name=version_name
    )


@router.post("/models/{model_name}/unload", response_model=bool)
async def unload_model(request: Request, model_name: str):
    return request.app.model.repository.unload_model(model_name)


@router.post(
    "/models/{model_name}/versions/{version_name}/unload", response_model=bool
)
async def unload_version(request: Request, model_name: str, version_name: str):
    return request.app.model.repository.unload_model(
        model_name, version_name=version_name
    )
