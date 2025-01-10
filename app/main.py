from fastapi import FastAPI, Request
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.endpoints import programs, auth, blog, gallery, partners
import uvicorn
from fastapi.staticfiles import StaticFiles
from decouple import config
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
DEBUG_MODE = config("DEBUG_MODE", default=False, cast=bool)

app = FastAPI(
    title="Lembaga Sinergi Analitika API",
    version="1.0.0"
)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Routes

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(programs.router, prefix="/programs", tags=["programs"])
app.include_router(blog.router, prefix="/blogs", tags=["blogs"])
app.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
app.include_router(partners.router, prefix="/partners", tags=["partners"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG_MODE
    )