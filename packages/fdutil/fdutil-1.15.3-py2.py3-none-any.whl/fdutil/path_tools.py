# encoding: utf-8

import os
import sys
import site
import subprocess

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'


def open_folder(path):
    try:
        if sys.platform == 'darwin':
            subprocess.check_call(['open', '--', path])
        elif sys.platform == 'linux2':
            subprocess.check_call(['xdg-open', '--', path])
        elif sys.platform == 'win32':
            subprocess.check_call(['explorer', path])

    except subprocess.CalledProcessError:
        pass  # Can sometimes fail on success on windows


def expand_path(path):

    if path.startswith(u'./'):
        path = u'{p}{s}{f}'.format(p=os.getcwd(),
                                   s=os.sep,
                                   f=path[2:])

    if u'/' in path and u'/' != os.sep:
        path = path.replace(u'/', os.sep)

    return path


def ensure_path_exists(path,
                       includes_filename=False):

    if includes_filename:
        # Discard filename
        path, _ = os.path.split(path)

    if not os.path.exists(path):
        os.makedirs(path)


def pop_path(path):

    """ Pops current folder / file from filepath and returns

    :param path: string:    Path to update
    :return: string:        new path
    """

    pth = path.split(os.sep)
    pth.pop()

    return os.sep.join(pth)


def generate_relative_html_link(src_dir,
                                linked_file):

    """

    :param src_dir:     The directory where the html file is
    :param linked_file: The file path to be referenced in the html file.
    :return:            Relative path valid in src_dir to the file.
    """

    # Validate src_dir is a directory
    if not os.path.isdir(src_dir):
        raise ValueError(u'src_dir should be a directory path!')

    if src_dir.endswith(os.sep):
        src_dir = src_dir[:-1]

    # Find common base of both paths
    common_pth = os.path.commonprefix([
        src_dir,
        os.path.dirname(linked_file)
    ])

    # update paths to remove the common base
    src_dir = src_dir.replace(common_pth, u'')
    linked_file = linked_file.replace(common_pth, u'')

    if linked_file.startswith(os.sep):
        # Remove the leading / from the output
        linked_file = linked_file[1:]

    # Work out how many levels we have to rise (if any) and create the prefix
    num_parts = len(src_dir.split(os.sep)) if src_dir != u'' else 0
    prefix = u'../' * num_parts if num_parts >= 1 else u'./'  # TODO: This is still not quite right!

    # create the relative path
    new_link_path = prefix + linked_file

    return new_link_path


def find_files(root_dir,
               extension=u'.html'):

    """ Finds all files with specified extension recursively under the root directory specified

    :param root_dir:    Directory to search
    :param extension:   File extension to search for
    :return:            List of file paths that match the search
    """

    matched_files = []

    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(extension):
                matched_files.append(os.path.join(root, f))

    return matched_files


def path_in_site_or_user_packages(path):
    """
    Returns True if the path matches the site or user packages paths
    :param path: path to a file or folder
    :return: Boolean
    """
    path = os.path.normpath(path)

    try:
        # site.getsitepackages() is not available in python 2.7 virtualenv's
        # https://github.com/pypa/virtualenv/issues/355
        site_paths = site.getsitepackages()

    except AttributeError:
        from distutils.sysconfig import get_python_lib
        site_paths = [
            get_python_lib()
        ]

    site_paths.append(site.USER_SITE)
    return any([path.startswith(site_path) for site_path in site_paths])
