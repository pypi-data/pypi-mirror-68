import io

import requests

from partial_web_file.file_util import get_partial_web_file_impl

SEEK_FROM_START = 0
SEEK_FROM_CURRENT_POSITION = 1
SEEK_FROM_END_OF_FILE = 2

DEFAULT_READ_CHUCK_SIZE = 1000000


class RemoteStream(io.BytesIO):
    """
    Imitates the bytes stream while each request for the real data is gotten from the remote website resource.
    """
    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._url = url
        self._cursor = 0

        with requests.get(self._url, stream=True) as r:
            self._length = int(r.headers['content-length'])
        if not self._length:
            raise Exception('Failed to get the length for resource ' + self._url)

    def seek(self, offset, whence=0):
        if whence == SEEK_FROM_START:
            self._cursor = offset
        elif whence == SEEK_FROM_CURRENT_POSITION:
            self._cursor += offset
        elif whence == SEEK_FROM_END_OF_FILE:
            self._cursor = self._length + offset
        else:
            raise ValueError("whence must be os.SEEK_SET (0), "
                             "os.SEEK_CUR (1), or os.SEEK_END (2)")

        if self._cursor > self._length:
            raise OSError("seek() position went over the size of a file")

        if self._cursor < 0:
            raise OSError("seek() position went below 0")

        return self.tell()

    def tell(self):
        return self._cursor

    def read(self, n=DEFAULT_READ_CHUCK_SIZE):
        count = min(n, self._length - self._cursor)
        data = get_partial_web_file_impl(self._url, self._cursor, count)
        self._cursor += len(data)
        return data
