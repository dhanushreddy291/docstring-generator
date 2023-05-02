import argparse
import logging
import re
import subprocess


def pip_show(package_name, packages=[]):
    """

    Recursively checks the dependencies of a given Python package using pip show command.

    Args:
        package_name (str): Name of the Python package to check the dependencies for.
        packages (list, optional): List of packages already checked to avoid checking the same package twice if multiple packages depend on it. Defaults to an empty list.

    Returns:
        None

    Raises:
        None

    """
    if package_name in packages:
        return  # avoid checking the same package twice if multiple packages depends on it.
    packages.append(package_name)

    result = subprocess.run(["pip", "show", package_name], stdout=subprocess.PIPE)
    if result.returncode != 0:
        logging.error("pip show %s failed", package_name)

    show_stdout = result.stdout.decode("utf-8")
    print(package_name + "==" + get_version(show_stdout))

    for dependency in get_dependencies(show_stdout):
        pip_show(dependency, packages=packages)


def get_version(show_stdout):
    """
    Returns the version of a Python package by parsing the output of pip show command.

    Args:
        show_stdout (str): Output of pip show command for a Python package.

    Returns:
        str: Version of the Python package.

    Raises:
        None
    """
    for line in show_stdout.split("\n"):
        m = re.match(r"^Version:\s(?P<version>.+)$", line)
        if m:
            return m.group("version")
    return "not found"


def get_dependencies(show_stdout):
    """
    Returns the list of dependencies of a Python package by parsing the output of pip show command.

    Args:
        show_stdout (str): Output of pip show command for a Python package.

    Returns:
        list: List of dependencies of the Python package.

    Raises:
        None
    """
    for line in show_stdout.split("\n"):
        m = re.match(r"^Requires:\s(?P<requires>.+)$", line)
        if m:
            return m.group("requires").split(", ")
    return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=str, help="package name")
    args = parser.parse_args()

    pip_show(args.package)
