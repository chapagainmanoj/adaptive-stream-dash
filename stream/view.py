"""
"""
import logging
from pathlib import Path
from sys import prefix
from uuid import uuid4
from starlette.responses import (
    StreamingResponse,
    JSONResponse,
    Response,
    FileResponse,
)
from starlette.endpoints import HTTPEndpoint
from stream.constants import REPRESENTATIONS
from stream.utils import parse_content_range, iter_content
from slugify import slugify
from datetime import date
import ffmpeg_streaming
from ffmpeg_streaming import Formats

CHUNK_SIZE = 512 * 512

logger = logging.getLogger(__name__)


class BasicStreamAPI(HTTPEndpoint):
    async def get(self, request):
        storage = request.app.state.storage
        database = request.app.state.database

        oid = request.path_params["oid"]
        video_obj = database.get(oid)
        try:
            video_file = Path(
                storage.path, video_obj.get("prefix"), video_obj.get("og_file")
            )
        except Exception as exc:
            logger.error(str(exc))
            return Response({"error": "Not found."}, status_code=404)
        size = video_file.stat().st_size
        range = request.headers.get("range")
        start, end, length = parse_content_range(range, size)
        return StreamingResponse(
            iter_content(video_file, start=start, end=end + 1),
            media_type="video/mp4",
            status_code=206,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(length),
                "Content-Range": f"bytes {start}-{end}/{size}",
            },
        )


class StorageMedia(HTTPEndpoint):
    async def get(self, request):
        database = request.app.state.database
        storage = request.app.state.storage
        oid = request.path_params["oid"]
        file_name = request.path_params["file_name"]
        # oid = request.path_params["oid"]
        video_obj = database.get(oid)
        path = Path(storage.path, video_obj.get("prefix"), oid, file_name)
        if not path.exists():
            return Response(status_code=404)
        return FileResponse(path)


class VideoAPI(HTTPEndpoint):
    async def get(self, request):
        database = request.app.state.database
        oid = request.path_params.get("oid")
        if oid:
            return JSONResponse(database.get(oid))
        return JSONResponse(database.list())

    async def post(self, request):
        form = await request.form()
        file = form["file"]
        filename = Path(file.filename)
        title = form["name"] or file.filename
        storage = request.app.state.storage
        database = request.app.state.database
        try:
            oid = uuid4().hex
            prefix = date.today().isoformat()
            path = storage.put(
                prefix=prefix, oid=oid, data_stream=file.file, suffix=filename.suffix
            )
            # Create DASH files

            video_path = Path(path)
            absolute_file = str(video_path.absolute())
            video = ffmpeg_streaming.input(absolute_file)

            dash = video.dash(Formats.h264())
            dash.representations(*REPRESENTATIONS)
            dash.output(absolute_file)

            # update db
            database.add(oid=oid, title=title, prefix=prefix, suffix=filename.suffix)
        except RuntimeError as exc:
            logger.error(exc)
            return Response(status_code=500)

        except Exception as exc:
            logger.error(exc)
            return Response(status_code=400)
        return JSONResponse({"message": "File uploaded"})
