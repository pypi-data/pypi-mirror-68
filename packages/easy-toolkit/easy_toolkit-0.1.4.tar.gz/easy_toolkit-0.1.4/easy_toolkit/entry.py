import importlib
from click.core import Command
import click
import os

# all command entries
@click.group()
def entry():
    pass


# scan all functions in the package toolkit and find out the type of "command", then import these functions
base_tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toolkit")
base_module_name = "easy_toolkit.toolkit"


def scan_all_command(parent_path, module_name):
    ret = []
    for child in os.listdir(parent_path):
        if child.startswith("__"):
            continue
        if os.path.isdir(os.path.join(parent_path, child)):
            ret.extend(scan_all_command(os.path.join(
                parent_path, child), ".".join([module_name, child])))
        else:
            if not child.endswith(".py"):
                continue
            ret.append(".".join([module_name, child])[:-3])
    return ret


r = scan_all_command(base_tools_path, base_module_name)

all_packages = [importlib.import_module(x) for x in r]
for x in all_packages:
    for d in dir(x):
        if d.startswith("__"):
            continue
        f_obj = getattr(x, d)
        if isinstance(f_obj, click.core.Command):
            entry.add_command(f_obj)


if __name__ == '__main__':
    entry()
