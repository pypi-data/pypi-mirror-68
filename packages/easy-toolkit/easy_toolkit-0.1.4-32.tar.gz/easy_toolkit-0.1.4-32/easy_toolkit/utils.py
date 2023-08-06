import os
import imghdr
import re
import click
import datetime
from urllib import parse
from posixpath import normpath
import asyncio


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
        new_file_name = file_name[:-3] + datetime.datetime.now().strftime("_%Y-%m-%d %H_%M_%S") + file_name[-3:]
        target = os.path.join(dir_path, new_file_name)
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
    with open(r"{}".format(target), "w", encoding="utf-8") as f:
        f.write(md_file_str)
        click.echo("save new file to: {}".format(target))


def screen_size():
    # 使用tkinter获取屏幕大小
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height


def current_dir():
    return os.getcwd()


class MeasuredEventLoop(asyncio.SelectorEventLoop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total_time = 0
        self._select_time = 0
        self._before_select = None
        self.warn_count = 0

    # TOTAL TIME:
    def run_forever(self):
        started = self.time()
        try:
            super().run_forever()
        finally:
            finished = self.time()
            self._total_time = finished - started
            print(f"Total spend time: {self._total_time:.{3}f}")

    # SELECT TIME:
    def _run_once(self):
        self._before_select = self.time()
        super()._run_once()

    def _process_events(self, *args, **kwargs):
        after_select = self.time()
        self._select_time += after_select - self._before_select
        if self._select_time > 10 * (self.warn_count + 1):
            print("This may take long, Please wait.")
            self.warn_count += 1
        super()._process_events(*args, **kwargs)

    # REPORT:
    def close(self, *args, **kwargs):
        super().close(*args, **kwargs)

        # select = self._select_time
        # cpu = self._total_time - self._select_time
        # total = self._total_time

        # print(f'Waited for select: {select:.{3}f}')
        # print(f'Did other stuff: {cpu:.{3}f}')
        # print(f'Total time: {total:.{3}f}')
