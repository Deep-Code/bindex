#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) DeepCode 2017, All Rights Reserved

All information contained herein is, and remains the property of DeepCode
and is provided to authorized clients Dissemination of this information
or reproduction of this material is strictly forbidden unless prior written
permission is obtained from DeepCode.
"""

from __future__ import print_function

import argparse
import json
import logging
import os
import sys

from bindex.const import *
from bindex.extractor import Extractor

__author__ = metadata.authors[0]
__copyright__ = metadata.copyright
__version__ = metadata.version
__license__ = metadata.license
__credits__ = metadata.authors
__maintainer__ = metadata.authors[0]
__email__ = metadata.emails[0]
__status__ = metadata.status

logger = logging.getLogger(__name__)


def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """
    author_strings = []
    for name, email in zip(metadata.authors, metadata.emails):
        author_strings.append('Author: {0} <{1}>'.format(name, email))

    epilog = '''
{project} {version}

{authors}
URL: <{url}>
'''.format(
        project=metadata.project,
        version=metadata.version,
        authors='\n'.join(author_strings),
        url=metadata.url)

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Argparse parameters.
    #
    arg_parser = argparse.ArgumentParser(
        prog=argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=metadata.description,
        epilog=epilog)

    arg_parser.add_argument(
        '-i', '--input-file',
        dest='input_file',
        required=True,
        help="Target file from which data will be extracted."
    )

    arg_parser.add_argument(
        '-d', '--definition-file',
        dest='definition_file',
        required=True,
        help="File definition the items to extract along with their positions."
    )

    arg_parser.add_argument(
        '-o', '--output-file',
        dest='output_file',
        default="output.json",
        help="Name of the file to contain the JSON-formatted results."
    )

    arg_parser.add_argument(
        '-v', '--verbose',
        dest='is_verbose',
        action="store_true",
        default=False,
        help="Display additional information about execution."
    )

    arg_parser.add_argument(
        '-V', '--version',
        action='version',
        version='{0} {1}'.format(metadata.project, metadata.version))

    args = arg_parser.parse_args(args=argv[1:])
    #
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    print(epilog)

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Basic Settings and argument validation
    #
    input_file = args.input_file
    definition_file = args.definition_file
    output_file = args.output_file
    is_verbose = args.is_verbose

    # Setup logging configuration
    logging_level = logging.INFO
    if is_verbose:
        logging_level = logging.DEBUG

    logging.basicConfig(format=LOG_FORMAT,
                        level=logging_level)

    logger.debug(os.getcwd())
    # Verify that the input file exists
    if not os.path.isfile(input_file):
        logger.error(MSG_ERROR_INPUT_FILE_NOT_FOUND.format(f=input_file))
        sys.exit(1)
    # Verify that the definition file exists
    if not os.path.isfile(definition_file):
        logger.error(MSG_ERROR_DEF_FILE_NOT_FOUND.format(f=definition_file))
        sys.exit(1)
    # Verify if the output file already exists
    if os.path.isfile(output_file):
        overwrite = input(ASK_OUTPUT_OVERWRITE)
        if overwrite != "Y":
            logger.warning(MSG_ERROR_OUTPUT_FILE_EXISTS)
            sys.exit(1)
    #
    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Program Execution
    #
    try:
        extractor = Extractor(
            _target_file=input_file,
            _definition_file=definition_file
        )
        result = extractor.extract()

        if result is not None:
            with open(output_file, "w+") as fp:
                json.dump(result, fp, indent=4, sort_keys=True)
            logger.info(MSG_INFO_FILE_SAVED.format(f=output_file))
        else:
            logger.info("No data extracted from '{f:s}'.".format(f=input_file))
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    logging.info(MSG_INFO_EXTRACTION_COMPLETE)

    return 0


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
