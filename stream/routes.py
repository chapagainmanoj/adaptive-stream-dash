from starlette.routing import Route, Mount
from stream.view import BasicStreamAPI, VideoAPI, StorageMedia
from starlette.staticfiles import StaticFiles


routes = [
    Route("/", StaticFiles(directory="static", html=True)),
    Mount("/static/", StaticFiles(directory="static"), name="static"),
    Route("/stream/{oid}", BasicStreamAPI),
    Route("/storage/{oid}/{file_name}", StorageMedia),
    Route("/video/", VideoAPI),
    Route("/video/{oid}", VideoAPI),
]
