from fastapi import APIRouter
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.responses import RedirectResponse

router = APIRouter()
openapi_url = "/openapi.json"
title = "Pinferencia"


@router.get(
    "/",
    response_class=RedirectResponse,
    include_in_schema=False,
)
async def home():
    return RedirectResponse(url="/docs")


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=title + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/theme-flattop.css",
    )


@router.get("/docs/oauth2-redirect", include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@router.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=openapi_url,
        title=title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
