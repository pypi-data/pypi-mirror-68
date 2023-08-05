import os
import imghdr
from urllib import parse
from posixpath import normpath


def get_home_path():
    return os.path.expanduser("~")


def urljoin(base, *url_paths):
<<<<<<< HEAD
    url_path = parse.quote("/".join(url_paths))
    return parse.urljoin(base, normpath(url_path))
=======
    url_path = "/".join(url_paths)
    return parse.quote(normpath(parse.urljoin(base, url_path)))
>>>>>>> 10850f7efb1f12410d59a92aa598350308d8c4ac


def is_image(file_path):
    ret = imghdr.what(file_path)
    return False if ret is None else True
