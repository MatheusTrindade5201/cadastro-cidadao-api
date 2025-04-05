from fastapi import APIRouter
from fastapi.responses import Response

home_router = APIRouter(tags=["home"])


@home_router.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)
