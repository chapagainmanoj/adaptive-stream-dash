import os
from typing import IO, Generator, Tuple


def parse_content_range(range: str, size: int) -> Tuple[int, int]:
    if not range:
        return 0, size - 1, size
    range = range.strip().lower()
    if not range.startswith("bytes"):
        return 0, size - 1, size
    range = range.split("=")[-1]
    start, end, *_ = map(str.strip, (range + "-").split("-"))

    start = max(0, int(start)) if start else 0
    end = min(size - 1, int(end)) if end else size - 1

    return start, end, end - start + 1


def iter_content(
    path: str,
    start: int = 0,
    end: int = None,
    block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0
    with open(path, "rb") as f:
        f.seek(start)
        while True:
            if end is not None and consumed + block_size > end:
                block_size = end - consumed + 1

            block = f.read(block_size)
            if not block:
                break

            yield block
            consumed += len(block)


def create_thumbnail(video, path):
    try:
        exit_code = os.system(
            f"ffmpeg -i {video} -ss 00:00:01.000 -vframes 1 {path}/thumbnail.png"
        )
        if exit_code != 0:
            raise Exception(f"FFMPEG Exit code : {exit_code}")
    except Exception as e:
        raise Exception(f"Could not create thumbnail for {video} : {e}")
