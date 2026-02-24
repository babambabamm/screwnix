import httpx
from fastapi import Request, HTTPException
from urllib.parse import urljoin
from screwnix.config.settings import TARGET_APP
from screwnix.core.logger import get_logger

logger = get_logger("Forwarder")

async def forward_request(request: Request):
    if not TARGET_APP:
        raise HTTPException(
            status_code=500,
            detail="TARGET_APP environment variable is not set"
        )

    target_url = TARGET_APP
    if not target_url.startswith(("http://", "https://")):
        target_url = f"http://{target_url}"

    full_url = urljoin(target_url, request.url.path)

    excluded_headers = {
        "host",
        "content-length",
        "connection",
        "transfer-encoding"
    }

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in excluded_headers
    }

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=10.0
        ) as client:

            body = await request.body()

            forwarded_response = await client.request(
                method=request.method,
                url=full_url,
                headers=headers,
                content=body,
                params=request.query_params
            )

            return forwarded_response

    except httpx.ConnectError as e:
        logger.error(f"Connection error to {target_url}: {e}")
        raise HTTPException(status_code=503, detail="Target unavailable")

    except httpx.TimeoutException as e:
        logger.error(f"Timeout error to {target_url}: {e}")
        raise HTTPException(status_code=504, detail="Target timeout")

    except Exception as e:
        logger.error(f"Unexpected proxy error: {e}")
        raise HTTPException(status_code=500, detail="Proxy forwarding error")