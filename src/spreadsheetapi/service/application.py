from fastapi import FastAPI
import v1

app = FastAPI()

app.include_router(v1.endpoints.router)
