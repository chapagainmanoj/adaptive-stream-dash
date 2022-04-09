from starlette.routing import Route
from .view import video_stream

routes = [
    Route("/stream/", video_stream),
]
