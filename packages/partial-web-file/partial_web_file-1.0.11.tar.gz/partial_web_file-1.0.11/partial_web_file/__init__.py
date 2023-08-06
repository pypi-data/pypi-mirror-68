import argparse
import os

import partial_web_file.file_util
import partial_web_file.zip_util


def get_partial_web_file(url, start_position, length):
    return partial_web_file.file_util.get_partial_web_file_impl(url, start_position, length)


def get_file_content_from_web_zip(zip_url, path_to_file_in_zip):
    """

    :param zip_url: url to zip in the web
    :param path_to_file_in_zip: path to the file in the remote zip to extract
    :return: content of the extracted file
    """
    return partial_web_file.zip_util.get_file_content_from_web_zip_impl(zip_url, path_to_file_in_zip)


def get_file_contents_from_web_zip(zip_url, paths_to_files_in_zip, on_content):
    """

    :param zip_url: url to zip in the web
    :param paths_to_files_in_zip: list of files to extract
    :param on_content: callback(path_to_file_in_zip, content), content is None if not found or error
    """
    partial_web_file.zip_util.get_file_contents_from_web_zip_impl(zip_url, paths_to_files_in_zip, on_content)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to zip')
    parser.add_argument('filenames', nargs=argparse.ONE_OR_MORE, help='files in zip to download to current folder')
    return parser.parse_args()


def main():
    args = _parse_args()

    url = args.url
    filenames = args.filenames

    def on_content(path, content):
        if content is None:
            print('Failed to download "%s"', path)
        else:
            save_to = os.path.basename(path)
            print('Saving %s:%s to %s...' % (url, path, save_to))
            with open(save_to, 'wb') as f:
                f.write(content)

    get_file_contents_from_web_zip(url, filenames, on_content)
    print('Done.')


if __name__ == '__main__':
    main()
