import os
from setuptools import setup, find_packages

md_path =os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")

setup(
    name='easy_toolkit',
    version='0.1.2',
    author="呆瓜",
    author_email="1032939141@qq.com",
    long_description=open(md_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'PyGithub>=1.51'
    ],
    entry_points='''
        [console_scripts]
        easytool=easy_toolkit.entry:entry
    ''',
    url="https://gitee.com/fadeaway_dai/convenient_toolkit"
)

# python setup.py sdist
# twine upload dist/*version*