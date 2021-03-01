from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import v1
from backends.exc import UnsupportedOperationForBackend

app = FastAPI()

app.include_router(v1.endpoints.router)

# Register status endpoint
@app.get("/status")
async def status():
    return ""


@app.exception_handler(UnsupportedOperationForBackend)
async def handle_unsupported_op_for_backend(
    request: Request, exc: UnsupportedOperationForBackend
):
    return JSONResponse(
        status_code=501,
        content={
            "error": "The configured backend does not support the "
            "requested operation"
        },
    )
