import os
from pathlib import Path
import shutil
from typing import Any, BinaryIO, Dict, Optional
from storage.core import StreamingStorage
from storage import exceptions as ext
from stream.utils import create_thumbnail


class LocalStorage(StreamingStorage):
    """Local storage implementation"""

    def __init__(self, path: str = None, **_):
        if path is None:
            path = "storage"
        self.path = Path(path)
        self._create_path(self.path)

    def get(self, prefix: str, oid: str) -> BinaryIO:
        path = self._get_path(prefix, oid)
        if os.path.isfile(path):
            return open(path, "br")
        else:
            raise ext.ObjectNotFound("Object was not found")

    def put(self, oid: str, prefix: str, data_stream: BinaryIO, suffix) -> int:

        path = self._get_path(prefix, oid)
        path = f"{path}/og{suffix}"
        directory = os.path.dirname(path)
        self._create_path(directory)
        with open(path, "bw") as dest:
            shutil.copyfileobj(data_stream, dest)

        create_thumbnail(path, directory)
        return path

    def exists(self, prefix: str, oid: str) -> bool:
        return os.path.isfile(self._get_path(prefix, oid))

    def get_size(self, prefix: str, oid: str) -> int:
        if self.exists(prefix, oid):
            return os.path.getsize(self._get_path(prefix, oid))
        raise ext.ObjectNotFound("Object was not found")

    def get_mime_type(self, prefix: str, oid: str) -> str:
        if self.exists(prefix, oid):
            return "application/octet-stream"
        raise ext.ObjectNotFound("Object was not found")

    def _get_path(self, prefix: str, oid: str) -> str:
        return os.path.join(self.path, prefix, oid)

    @staticmethod
    def _create_path(path):
        if not os.path.isdir(path):
            os.makedirs(path)
