from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz():
    return True
