from setuptools import setup, find_packages

setup(
    name='easy_toolkit',
    version='0.1',
    author="呆瓜",
    author_email="1032939141@qq.com",
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
)
