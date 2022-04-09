from starlette.routing import Route, Mount
from stream.view import video_stream
from starlette.staticfiles import StaticFiles


routes = [
    Route("/", StaticFiles(directory="static", html=True)),
    Route("/stream/", video_stream),
]
