import os
from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easy_toolkit',
    version='0.1.5.1',
    author="呆瓜",
    author_email="1032939141@qq.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=
    [
        'Click',
        'PyGithub==1.51',
        'requests',
        'asyncclick==7.0.9',
        'pyppeteer==0.2.2',
        'trio==0.14.0'
    ],
    entry_points='''
        [console_scripts]
        easytool=easy_toolkit.entry:entry
    ''',
    url="https://gitee.com/fadeaway_dai/convenient_toolkit"
)

# python setup.py sdist
# twine upload dist/*version*
