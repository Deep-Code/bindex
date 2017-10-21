#!/usr/bin/env python
# coding: utf-8
"""
    bindex.const
    ~~~~~~~~~~~~~

    Contains a set of constants used across the application. All strings and constants
    should be accessible from this file to prevent modifying the code modules.

    :copyright: 2017, Jonathan Racicot, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
__author__ = "Jonathan Racicot"
__copyright__ = "Copyright 2017, DeepCode"
__credits__ = ["Jonathan Racicot"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Jonathan Racicot"
__email__ = "jon@deepcode.ca"
__status__ = "Development"

#
# In order to avoid modifying the remainder of the application, do not
# change the name of the parameters in the strings. However you can modify the messages
# as needed.
#

EMPTY_STRING = ""
NO_VALUE = None
ERROR_VALUE = "Error!"
LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"
DATETIME_STAMP = "{cdate:s}:{ctime:s}"

PARAM_METADATA = "meta"
PARAM_META_AUTHOR = "author"
PARAM_META_DESC = "description"
PARAM_META_VERSION = "version"
PARAM_META_DATE = "creation_date"
PARAM_COMPATIBILITY_PARAMS = "compatibility"
PARAM_OTHER_PARAMS = "parameters"

METADATA = [
    PARAM_META_AUTHOR,
    PARAM_META_DESC,
    PARAM_META_VERSION,
    PARAM_META_DATE,
    PARAM_COMPATIBILITY_PARAMS,
    PARAM_OTHER_PARAMS
]

PARAM_NAME = "name"
PARAM_SIZE = "size"
PARAM_OFFSET = "offset"
PARAM_RELATIVE = "relative_to"
PARAM_TYPE = "type"
PARAM_VALUE = "value"
PARAM_COMPATIBLE_WITH = "compatible_with"
PARAM_ORIGINAL_FILE = "target"
PARAM_DEF_FILE = "definition"
PARAM_ANALYSIS_DATE = "analyzed_on"
PARAM_ORIGINAL_FILE_HASH = "sha1"

NAME_UNKNOWN = "unknown"
UNKNOWN_PARAM_FORMAT = "{prefix:s}{idx:03d}"

COMPATIBILITY_MANDATORY_VALUES = [
    PARAM_NAME,
    PARAM_SIZE,
    PARAM_OFFSET,
    PARAM_TYPE,
    PARAM_COMPATIBLE_WITH
]

PARAMETER_STR = "Parameter '{pn:s}', {type:s} of {sz:d} byte(s) at 0x{off:08X} byte(s) from '{rn:s}'."
PARAMETER_REPR = "<Parameter Name='{n:s}', Offset=0x{off:08X}, Size={sz:d} byte(s), RelativeTo:{rn:s}, Type={type:s}, Value={val:s}"
EXTRACTOR_REPR = "<Extractor definition='{df:s}', target='{tf:s}'>"
TARGET_FILE_REPR = "<TargetFile file='{f:s}'.>"

ABSTRACT_FILE_REPR = "<AbstractFile File='{f:s}'>"
DEFINITION_FILE_REPR = "<DefinitionFile File='{f:s}'>"

TYPE_ASCII = "ascii"
TYPE_UTF8 = "utf-8"
TYPE_UTF16 = "utf-16"

TYPE_STRING = [TYPE_ASCII, TYPE_UTF8, TYPE_UTF16]

ASK_OUTPUT_OVERWRITE = "The chosen output file already exists, overwrite it? [Y/n]"
MSG_INFO_LOADING_DEF_FILE = "Loading definition file from '{f:s}'..."
MSG_INFO_EXTRACTION_COMPLETE = "Extraction completed."
MSG_ERROR_INCOMPLETE_PARAM = "Missing mandatory properties in parameters. Cannot parse into object."
MSG_ERROR_READ_PARAM = "Failed to read parameter '{param:s}'."
MSG_ERROR_INPUT_FILE_NOT_FOUND = "Could not find the input file: '{f:s}'."
MSG_ERROR_DEF_FILE_NOT_FOUND = "Could not find the definition file: '{f:s}'."
MSG_ERROR_NOT_COMPATIBLE = "Definition file is not compatible with target file."
MSG_ERROR_OUTPUT_FILE_EXISTS = "Output file with similar name exists."
MSG_ERROR_NO_DATA_EXTRACTED = "No data was extracted from '{f:s}'."
