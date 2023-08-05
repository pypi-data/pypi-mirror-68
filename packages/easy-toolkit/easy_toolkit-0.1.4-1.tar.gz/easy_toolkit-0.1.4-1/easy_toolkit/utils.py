import os
import imghdr
from urllib import parse
from posixpath import normpath


def get_home_path():
    return os.path.expanduser("~")


def urljoin(base, *url_paths):
    url_path = parse.quote("/".join(url_paths))
    return parse.urljoin(base, normpath(url_path))


def is_image(file_path):
    ret = imghdr.what(file_path)
    return False if ret is None else True
