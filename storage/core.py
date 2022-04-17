from mimetypes import guess_extension, guess_type
from abc import ABC
from typing import Any, BinaryIO, Dict, Iterable, Optional
from storage.exceptions import ObjectNotFound


class VerifiableStorage(ABC):
    """A storage backend that supports object verification API
    All streaming backends should be 'verifiable'.
    """

    def verify_object(self, prefix: str, oid: str, size: int) -> bool:
        """Check that object exists and has the right size
        This method should not throw an error if the object does not exist, but return False
        """
        pass


class StreamingStorage(VerifiableStorage, ABC):
    """Interface for streaming storage adapters"""

    def get(self, prefix: str, oid: str) -> Iterable[bytes]:
        pass

    def put(self, prefix: str, oid: str, data_stream: BinaryIO) -> int:
        pass

    def exists(self, prefix: str, oid: str) -> bool:
        pass

    def get_size(self, prefix: str, oid: str) -> int:
        pass

    def get_mime_type(self, prefix: str, oid: str) -> Optional[str]:
        return "application/octet-stream"

    def verify_object(self, prefix: str, oid: str, size: int):
        """Verify that an object exists"""
        try:
            return self.get_size(prefix, oid) == size
        except ObjectNotFound:
            return False


def guess_mime_type_from_filename(filename: str) -> Optional[str]:
    return guess_type(filename)[0]


def guess_extension_from_type(content_type: str) -> Optional[str]:
    return guess_extension(content_type)
