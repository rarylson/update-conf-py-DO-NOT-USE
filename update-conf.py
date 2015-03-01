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
__program__ = "update-conf.py"
__version__ = "0.3.2"
__license__ = "Revised BSD"

# Consts
DEFAULT_CONFIG = "/etc/{0}.conf".format(__program__)
DEFAULT_DIR_EXT = "d"
DEFAULT_COMMENT_PREFIX = "#"
IGNORE_FILES_EXT = ["bak", "backup", "old", "inactive", "disabled"]
BACKUP_EXT = "bak"

# Flags
VERBOSE = False


# Print a message if verbose is set
def _print_verbose(message):
    if VERBOSE:
        print(message)


# Print an error message and then exit
#
# This function exit with an adequate exit code
def _error(message):
    print("Error: {0}".format(message), file=sys.stderr)
    sys.exit(1)


# Create a auto-generated comment
#
# The comment can be used after when generating a config file.
# The prefix param is used to set the prefix of the comment. Common values
# are '#', ';' and '//'.
# It returns the comment.
def _autogenerated_comment(prefix):
    MESSAGE = "Auto-generated by {0}".format(__program__)
    WARNING = ("Do NOT edit this file by hand. Your changes will be "
               "overwritten.")

    comment = "{0} {1}\n{0} {2}\n".format(prefix, MESSAGE, WARNING)

    return comment


# Parse command line args and config file
#
# The config file to be parsed is the program default or passed via command
# line args.
# An error message and the usage will be printed and the program will exit if
# any parser error occur.
# It returns a argparse 'args' object.
def _parse_all():
    args = None
    global VERBOSE

    # Parse args
    parser = argparse.ArgumentParser(
        description="Generate config files from 'conf.d' like directories")
    parser.add_argument(
        "-f", "--file", help="config file to be generated")
    parser.add_argument(
        "-d", "--dir",
        help="directory with the splitted files (default "
             "FILE.{0})".format(DEFAULT_DIR_EXT))
    parser.add_argument(
        "-n", "--name",
        help="name of the section (defined in the config file) to be used")
    parser.add_argument(
        "-c", "--config",
        help="{0} config file (default {0})".format(
            __program__, DEFAULT_CONFIG),
        default=DEFAULT_CONFIG)
    parser.add_argument(
        "-p", "--comment-prefix",
        help="Prefix to be used in the auto-generated comment (default '#')")
    parser.add_argument(
        "-v", "--verbose", action="store_true")
    parser.add_argument(
        "-V", "--version", action="version", version=__version__)
    args = parser.parse_args()

    # Set global verbose flag
    VERBOSE = args.verbose

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
        if (not args.comment_prefix and
                config_parser.has_option(args.name, 'comment_prefix')):
            args.comment_prefix = config_parser.get(
                args.name, 'comment_prefix')

    # More parse errors
    if not args.file:
        parser.error(
            "'file' is required (you must set it via config file or command "
            "line arguments)")

    # Default values
    if not args.dir:
        args.dir = "{0}.{1}".format(args.file, DEFAULT_DIR_EXT)
    if not args.comment_prefix:
        args.comment_prefix = DEFAULT_COMMENT_PREFIX

    _print_verbose(
        "Generating {0} using splitted config files from {1}...".format(
            args.file, args.dir))

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
                    _print_verbose("Skiping {0}".format(entry))
                    entry_is_valid = False
                    break
            if entry_is_valid:
                splitted_files.append(entry_path)
    # Dir not found error
    except OSError:
        _error("Dir '{0}' not found".format(directory))
    # No splitted files error
    if not splitted_files:
        _error("No splitted files found in dir '{0}'".format(directory))

    return splitted_files


# Create a temp config file
#
# This funtion merges all splited files into a new and temporary file.
# It returns the path to the newly created temporary file.
def _create_temp_config(splitted_files, comment_prefix):
    temp_file = None

    temp_file_fd, temp_file = tempfile.mkstemp()
    # Convert 'temp_file_fd' to a Python file object
    # See: http://www.logilab.org/blogentry/17873
    temp_file_fd = os.fdopen(temp_file_fd, 'w')
    # Insert a autogenerated comment (with a newline to improve readability)
    comment = "{0}\n".format(_autogenerated_comment(comment_prefix))
    temp_file_fd.write(comment)
    # Merge files
    for splitted in splitted_files:
        _print_verbose("Merging {0}".format(splitted))
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
        _print_verbose("Backing up current {0}".format(config_file))
        os.rename(config_file, "{0}.{1}".format(config_file, BACKUP_EXT))
    # Move temp_file
    # Using shutil.move because the tmp file can be in a different filesystem
    _print_verbose("Generating {0}".format(config_file))
    shutil.move(temp_file, config_file)
    _print_verbose("Done")


# Run the script
def run():
    args = _parse_all()
    splitted_files = _get_splitted(args.dir)
    temp_file = _create_temp_config(splitted_files, args.comment_prefix)
    _temp_to_file(temp_file, args.file)


if __name__ == "__main__":
    run()
