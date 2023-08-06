import logging
import zipfile

from partial_web_file.remote_stream import RemoteStream


LOG = logging.getLogger("PARTIAL_WEB_FILE")


def _get_file_content_from_web_zip_impl(stream, path_to_file_in_zip):
    try:
        with zipfile.ZipFile(stream, 'r') as zf:
            return zf.read(path_to_file_in_zip)
    except Exception as e:
        LOG.error(e)
        return None


def get_file_content_from_web_zip_impl(zip_url, path_to_file_in_zip):
    stream = RemoteStream(zip_url)
    return _get_file_content_from_web_zip_impl(stream, path_to_file_in_zip)


def get_file_contents_from_web_zip_impl(zip_url, paths_to_files_in_zip, on_content):
    stream = RemoteStream(zip_url)
    with zipfile.ZipFile(stream, 'r') as zf:
        for path_to_file_in_zip in paths_to_files_in_zip:
            content = _get_file_content_from_web_zip_impl(stream, path_to_file_in_zip)
            on_content(path_to_file_in_zip, content)
