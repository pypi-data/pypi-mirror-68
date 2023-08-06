"""
Main CLI entry point.
"""
import argparse
import os
import shutil


def create_package_dir(package_name):
    """
    Main function to create a basic python package directory.

    :param str package_name: the intended package name
    """
    template_pkg_name = os.path.join(os.path.dirname(__file__), "template")
    new_pkg_name = os.path.join(os.getcwd(), package_name)
    shutil.copytree(template_pkg_name, package_name)
    os.rename(os.path.join(new_pkg_name, "template"), os.path.join(new_pkg_name, package_name))


def main():
    """
    Main runner for CLI.
    """
    parser = argparse.ArgumentParser(description='create python package skeleton')
    parser.add_argument('name', help='name of the package')
    args = parser.parse_args()
    if "name" in args:
        create_package_dir(args.name)
