from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get(
    "/",
    response_class=RedirectResponse,
    include_in_schema=False,
)
async def home():
    return RedirectResponse(url="/docs")


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    return get_swagger_ui_html(
        openapi_url=request.app.openapi_url,
        title=request.app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url=f"/static/theme-{request.app.swagger_theme}.css",
    )
