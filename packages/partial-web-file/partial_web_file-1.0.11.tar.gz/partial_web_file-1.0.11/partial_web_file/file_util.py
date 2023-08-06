import logging
import requests
from functools import lru_cache


LOG = logging.getLogger("PARTIAL_WEB_FILE")

session = requests.Session()


@lru_cache(maxsize=30)
def get_partial_web_file_impl(url, start_position, length):
    headers = {"Range": "bytes=%d-%d" % (start_position, start_position + length - 1)}
    r = session.get(url, headers=headers)
    data = r.content
    data_len = len(data)
    if data_len != length:
        LOG.warning(
            'Web returned %d while asked only for %d... Does this Web server support the "Range" header?'
            % (data_len, length)
        )
        return data[start_position:start_position + length]
    else:
        return data
