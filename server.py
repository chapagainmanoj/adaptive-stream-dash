from starlette.applications import Starlette
from starlette.config import Config
from storage.local import LocalStorage
from stream.routes import routes
from database.db import VideoDatabase

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)


def startup():
    storage = LocalStorage(config("STORAGE_PATH"))
    database = VideoDatabase()
    app.state.storage = storage
    app.state.database = database


app = Starlette(debug=DEBUG, routes=routes, on_startup=[startup])
