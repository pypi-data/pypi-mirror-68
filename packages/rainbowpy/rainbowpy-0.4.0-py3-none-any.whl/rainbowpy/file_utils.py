import os
import shutil
import tempfile
import uuid
from contextlib import contextmanager
from shutil import copyfile

import pkg_resources


def get_path_of_data_file(data_file):
    file_path = pkg_resources.resource_filename(
        "rainbowpy", "data/%s" % data_file)

    return file_path


def get_path_of_data_dir():
    file_path = pkg_resources.resource_filename("rainbowpy", "data")

    return file_path


def copy_package_data(data_file):

    data_file_path = get_path_of_data_file(data_file)
    copyfile(data_file_path, "./%s" % data_file)


def get_path_of_user_dir():
    """
    Returns the path of the directory containing the user data (~/.rainbowpy)

    :return: an absolute path
    """

    return os.path.abspath(os.path.expanduser("~/.rainbowpy"))


def file_existing_and_readable(filename):

    sanitized_filename = sanitize_filename(filename)

    if os.path.exists(sanitized_filename):

        # Try to open it

        try:

            with open(sanitized_filename):

                pass

        except:

            return False

        else:

            return True

    else:

        return False


def path_exists_and_is_directory(path):

    sanitized_path = sanitize_filename(path, abspath=True)

    if os.path.exists(sanitized_path):

        if os.path.isdir(path):

            return True

        else:

            return False

    else:

        return False


def sanitize_filename(filename, abspath=False):

    sanitized = os.path.expandvars(os.path.expanduser(filename))

    if abspath:

        return os.path.abspath(sanitized)

    else:

        return sanitized


def if_directory_not_existing_then_make(directory):
    """
    If the given directory does not exists, then make it
    :param directory: directory to check or make
    :return: None
    """

    sanitized_directory = sanitize_filename(directory)

    if not os.path.exists(sanitized_directory):

        os.makedirs(sanitized_directory)


@contextmanager
def within_directory(directory):

    current_dir = os.getcwd()

    if not os.path.exists(directory):

        raise IOError("Directory %s does not exists!" %
                      os.path.abspath(directory))

    try:
        os.chdir(directory)

    except OSError:

        raise IOError("Cannot access %s" % os.path.abspath(directory))

    yield

    os.chdir(current_dir)
