from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get(
    "/",
    response_class=RedirectResponse,
    include_in_schema=False,
)
async def home():
    return RedirectResponse(url="/docs")
