#!/usr/bin/env python

"""Generate config files from 'conf.d' like directories

Split your config file into smaller files in a 'conf.d' like directory.

NOTE: This software was based in the 'update-conf.d' project.
      See: https://github.com/Atha/update-conf.d
"""

from __future__ import print_function

import sys
import os
import shutil
import tempfile

import argparse
from ConfigParser import SafeConfigParser

# About
__author__ = "Rarylson Freitas"
__email__ = "rarylson@gmail.com"
__version__ = "0.1.0"

# Consts
DEFAULT_CONFIG = "/etc/update-conf.py.conf"
DEFAULT_DIR_EXT = "d"
IGNORE_FILES_EXT = ["bak", "backup", "old", "inactive"]
BACKUP_EXT = "bak"


# Parse command line args and config file
#
# The config file to be parsed is the program default or passed via command
# line args.
# An error message and the usage will be printed and the program will exit if
# any parser error occur.
# It returns a argparse 'args' object.
def _parse_all():
    args = None

    # Parse args
    parser = argparse.ArgumentParser(
        description="Generate config files from 'conf.d' like directories")
    parser.add_argument(
        "-f", "--file", help="config file to be generated")
    parser.add_argument(
        "-d", "--dir",
        help="directory whith the splitted files (default "
             "FILE_PATH/FILE_NAME.{0})".format(DEFAULT_DIR_EXT))
    parser.add_argument(
        "-n", "--name",
        help="name of the section (defined in the config file) to be used "
             "while generating a config file")
    parser.add_argument(
        "-c", "--config",
        help="update-conf.py config file (default {0})",
        default=DEFAULT_CONFIG)
    parser.add_argument(
        "-v", "--version", action="version", version=__version__)
    args = parser.parse_args()

    # Parse config file
    if args.name:
        config_parser = SafeConfigParser()
        # Open config file
        try:
            config_parser.readfp(open(args.config, 'r'))
        except IOError:
            parser.error("config file '{}' not found".format(args.config))
        # Section not found error
        if not config_parser.has_section(args.name):
            parser.error(
                "section name '{}' not found in config file".format(args.name))
        # Get options from config file (options from command line take
        # precedence)
        if not args.file and config_parser.has_option(args.name, 'file'):
            args.file = config_parser.get(args.name, 'file')
        if not args.dir and config_parser.has_option(args.name, 'dir'):
            args.dir = config_parser.get(args.name, 'dir')

    # More parse errors
    if not args.file:
        parser.error(
            "'file' is required (you must set it via config file or cmd arg)")

    # Default value of 'dir'
    if not args.dir:
        args.dir = "{0}.{1}".format(args.file, DEFAULT_DIR_EXT)

    return args


# Get all valid splitted files inside a dir
#
# This funtion skips all entries that are not files or end with some special
# extensions.
# An error message will be printed and the program will exit if any error
# occur.
# It returns a list will all splitted files.
def _get_splitted(directory):
    splitted_files = []

    # Test all entries in the dir, getting the spllited files
    try:
        entries = os.listdir(directory)
        # Sort the return of 'listdir' as "the list is in arbitrary order"
        # acourding to the docs. The explanation comes from the SO underlying
        # implementation.
        # See: https://docs.python.org/2/library/os.html#os.listdir
        #      http://stackoverflow.com/a/8984803/2530295
        entries.sort()
        for entry in entries:
            entry_path = os.path.join(directory, entry)
            entry_is_valid = True
            if not os.path.isfile(entry_path):
                continue
            for ext in IGNORE_FILES_EXT:
                if entry.endswith(ext):
                    entry_is_valid = False
                    break
            if entry_is_valid:
                splitted_files.append(entry_path)
    # Dir not found error
    except OSError:
        print("Error: Dir '{0}' not found".format(directory))
        sys.exit(1)
    # No splitted files error
    if not splitted_files:
        print("Error: No splitted files found in dir '{0}'".format(directory))
        sys.exit(1)

    return splitted_files


# Create a temp config file
#
# This funtion merges all splited files into a new and temporary file.
# It returns the path to the newly created temporary file.
def _create_temp_config(splitted_files):
    temp_file = None

    temp_file_fd, temp_file = tempfile.mkstemp()
    # Convert 'temp_file_fd' to a Python file object
    # See: http://www.logilab.org/blogentry/17873
    temp_file_fd = os.fdopen(temp_file_fd, 'w')
    for splitted in splitted_files:
        with open(splitted, 'r') as splitted_fd:
            temp_file_fd.write(splitted_fd.read())
    temp_file_fd.close()

    return temp_file


# Move a temp config file to your final location
#
# This function makes a backup of the current config file and then puts the
# new file (currently a temp file) to the final config file location.
def _temp_to_file(temp_file, config_file):
    # Backup
    if os.path.isfile(config_file):
        os.rename(config_file, "{0}.{1}".format(config_file, BACKUP_EXT))
    # Move temp_file
    # Using shutil.move because the tmp file can be in a different filesystem
    shutil.move(temp_file, config_file)


# Run the script
def run():
    args = _parse_all()
    spplited_files = _get_splitted(args.dir)
    temp_file = _create_temp_config(spplited_files)
    _temp_to_file(temp_file, args.file)


if __name__ == "__main__":
    run()
