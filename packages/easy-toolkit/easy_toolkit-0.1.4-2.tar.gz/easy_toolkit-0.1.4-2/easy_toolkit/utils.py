import os
import imghdr
import re
import click
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


def transfer_md(file, upload_func, head, target=None):
    if not head:
        head = "http"
    if not target:
        dir_path, file_name = os.path.split(file)
        new_file_name = file_name[:-3] + '_copy' + file_name[-3:]
        target = os.path.join(dir_path, new_file_name)
    new_md_file = target
    # 1.读取md文件,并找出其中非http开头的图片
    with open(file, "r", encoding="utf-8") as f:
        md_file_str = f.read()
        # 1.1正则匹配出其中的图片的本地path
        path_list = re.findall(r"!\[.*\]\((.*)\)", md_file_str)
        # path_list2 = re.findall(r"<img\s+src=\"(.*?)\".*/>", md_file_str) or []
        path_list2 = re.findall(r'''<img\s+src=\"(.*?)\"''', md_file_str) or []
        path_list.extend(path_list2)
        # 1.2读取并上传本地文件
        for p in path_list:
            if p.startswith(r"" + head):
                continue
            url_link = upload_func(p)
            # 1.3替换原有的本地链接
            # md_file_str = re.sub(r"{}".format(p), url_link, md_file_str)
            md_file_str = md_file_str.replace(p, url_link)
            click.echo("replacing [{}] to [{}]".format(p, url_link))
    # 2.重新写入文件
    with open(new_md_file, "w") as f:
        f.write(md_file_str)
        click.echo("save new file to: {}".format(new_md_file))