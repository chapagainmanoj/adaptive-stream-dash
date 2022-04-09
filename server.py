from starlette.applications import Starlette

from stream.routes import routes


app = Starlette(debug=True, routes=routes)
