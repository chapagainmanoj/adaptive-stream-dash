from pathlib import Path
from starlette.responses import StreamingResponse

from stream.utils.video_content import parse_content_range, iter_content

CHUNK_SIZE = 512 * 512
PROJECT_PATH = Path.cwd()
VIDEO_PATH = Path(PROJECT_PATH, "media/fire.mp4")


async def video_stream(request):

    file_size = VIDEO_PATH.stat().st_size

    range = request.headers.get("range")
    start, end, length = parse_content_range(range, file_size)
    headers = {}

    if range:
        file = iter_content(VIDEO_PATH, start=start, end=end + 1)
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"

    response = StreamingResponse(
        file,
        media_type="video/mp4",
        status_code=206,
    )

    response.headers.update(
        {
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            **headers,
        }
    )

    return response
