from starlette.responses import JSONResponse


async def video_stream(request):
    return JSONResponse({"hello": "world"})
