#Entry route for proxy
from fastapi import APIRouter, Request, Response
from screwnix.proxy.forwarder import forward_request
from screwnix.core.logger import get_logger

router = APIRouter()
logger = get_logger("Proxy")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    logger.info(f"Intercepted {request.method} request to /{path}")

    forwarded_response = await forward_request(request)

    logger.info(f"Response status: {forwarded_response.status_code}")

    return Response(
        content=forwarded_response.content,
        status_code=forwarded_response.status_code,
        headers=dict(forwarded_response.headers)
    )