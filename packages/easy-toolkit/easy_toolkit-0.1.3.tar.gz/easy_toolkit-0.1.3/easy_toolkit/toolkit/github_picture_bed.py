# github作为图床

import os
import sys
import click

from easy_toolkit.default_settings import SettingsHandler
from easy_toolkit.utils import urljoin, is_image

import github
from github import Github

@click.command(name="gitpic")
@click.option('-f', '--file', required=True,  help='Your pic path')
@click.option('-m', '--message', default="",  help='commit message')
@click.option('-n', '--name', default="",  help='Picture name')
def hello(file, message, name):
    if not os.path.exists(file):
        click.echo(click.style("File [{}] not exists", fg="red").format(file))
        sys.exit(1)
    if not is_image(file):
        click.echo(click.style("Please choose a image type file!", fg="red"))
        sys.exit(1)
    if not name:
        name = os.path.basename(file)
    if not message:
        message = "add picture {}".format(name)

    raw_base_url = "https://raw.githubusercontent.com/"
    repo_branch = "master"

    # using username and password
    github_token = SettingsHandler.read_property("github_token")
    if not github_token:
        github_username, github_password = SettingsHandler.read_property("github_username"), SettingsHandler.read_property("github_password")
        if not all([github_username, github_password]):
            click.echo(click.style("Please set [github_token] or [github_username、github_password] before use gitpic!", fg="red"))
            sys.exit(1)
        else:
            g = Github(github_username, github_password)
    else:
        g = Github(github_token)

    # repo_name = "fadeawaylove/article-images"
    repo_name = SettingsHandler.read_property("github_reponame")
    if repo_name is None:
        click.echo(click.style("Please set [github_reponame] before use gitpic!", fg="red"))
        sys.exit(1)
    # Then play with your Github objects:
    picture_repo = g.get_repo(repo_name)

    file_name = name
    file_path = file
    try:
        ret = picture_repo.create_file(path=file_name, message=message, content=open(file_path, 'rb').read(), branch="master")["content"]
    except Exception as e:
        if e.status == 422:
            # 文件名 已经存在 返回存在文件的路径
            click.echo(click.style("file [{}] already exists!", fg="red").format(name), )
            ret = picture_repo.get_contents(name)
            file_raw_url = urljoin(raw_base_url, repo_name, repo_branch, ret.path)
            click.echo("raw path ==> {}".format(file_raw_url))
        else:
            click.echo(e)
        sys.exit(1)
        
    file_raw_url = urljoin(raw_base_url, repo_name, repo_branch, ret.path)
    click.echo("upload success ==> {}".format(file_raw_url))
    return file_raw_url