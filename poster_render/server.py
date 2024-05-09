import uvicorn
from fastapi import FastAPI

from config import settings
from poster_render.routers import poster_router


class Server:
    def __init__(self):
        self.app = FastAPI()
        self.host = settings.HOST
        self.port = settings.PORT

    def init_app(self):
        self.app.include_router(poster_router.router, prefix="/api/v1/poster", tags=["Poster"])

    def run(self):
        uvicorn.run(
            app=self.app,
            host=self.host,
            port=self.port,
        )
