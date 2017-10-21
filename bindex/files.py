#!/usr/bin/env python
# coding: utf-8
"""
    bindex.files
    ~~~~~~~~~~~~~

    A description which can be long and explain the complete
    functionality of this module even with indented code examples.
    Class/Function however should not be documented here.

    :copyright: 2017, Jonathan Racicot, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import hashlib
import json
import logging
import os
import struct

from bindex.const import *
from bindex.parameter import CompatibilityParameter
from bindex.parameter import Parameter

__author__ = "Jonathan Racicot"
__copyright__ = "Copyright 2017, DeepCode"
__credits__ = ["Jonathan Racicot"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Jonathan Racicot"
__email__ = "jon@deepcode.ca"
__status__ = "Development"

logger = logging.getLogger(__name__)


class AbstractFile(object):
    def __init__(self, _file):
        assert os.path.isfile(_file)
        self.__file = _file

    def __repr__(self):
        s = ABSTRACT_FILE_REPR.format(
            f=self.file
        )
        return s

    def __str__(self):
        """
        Returns the path and filename of the definition. Same as calling x.file
        :return: The absolute path of the file.
        """
        s = self.__file
        return s

    @property
    def file(self):
        """
        Returns the path and filename of the definition.
        :return: The absolute path of the file.
        """
        return self.__file


class DefinitionFile(AbstractFile):
    """
    The DefinitionFile object holds the data parsed from the file containing
    data about how to extract details from the target file.
    """

    def __init__(self, _file):
        """
        Creates and parses a DefinitionFile object from the given path to a file.
        :param _file: An absolute path to a JSON-formatted file containing the definition.
        """
        super().__init__(_file)
        self.__meta = {}
        self.__compatibility = {}
        self.__parameters = {}

        self.__load_definition()

    def __repr__(self):
        """
        Returns a string representation of the DefinitionFile object.
        :return: A string representation of the DefinitionFile object.
        """
        s = DEFINITION_FILE_REPR.format(
            f=self.file
        )
        return s

    @property
    def parameters(self):
        """
        Returns a dictionary of parameters defined in the file

        This function will return a dictionary in which keys represent
        the name of the parameter and the values the parameter object. For
        example:

        {
            "file_size" : <Parameter Object>
        }

        The dictionary will not contain the parameters used to validate the
        compatibility of the target file. These can be retrieved using
        DefinitionFile.compatibility

        :return: A dictionary of parameters to extract
        """
        return self.__parameters

    @property
    def compatibility(self):
        """
        Returns a dictionary of parameters used to check compatibility with the
        target file.

        This function will return a dictionary in which keys represent
        the name of the parameter and the values the parameter object. For
        example:

        {
            "version" : <Parameter Object>
        }

        The dictionary will not contain the other parameters to extract from
        the target file. These can be retrieved using DefinitionFile.parameters

        :return: A dictionary of parameters to validate compatibility.
        """
        return self.__compatibility

    def related(self, _parameter):
        """
        If the given parameter is related to another parameter, this function will
         return the related Parameter object. Returns None if no the parameters is
         not related to anything.
        :param _parameter: The parameter
        :return: The related Parameter object or None.
        """
        assert isinstance(_parameter, Parameter)

        if _parameter.relative_to in self.compatibility.keys():
            return self.compatibility[_parameter.relative_to]
        elif _parameter.relative_to in self.parameters.keys():
            return self.parameters[_parameter.relative_to]
        else:
            return None

    def __load_definition(self):
        """
        This function is responsible for parsing the file containing the JSON
        data specifying how to extract data from the target file. The results
        are stored into members of the object.

        :return: None
        """
        # Ensure the encapsulate file is actually a file...
        assert os.path.isfile(self.file)
        logger.info(MSG_INFO_LOADING_DEF_FILE.format(f=self.file))

        with open(self.file, "r") as fp:
            # Load the JSON contents of the file.
            data = json.load(fp)

            # Load the metadata first, if any
            for meta_item in METADATA:
                if meta_item in data:
                    logger.debug("\t{pname:<16s}:{pvalue}".format(
                        pname=meta_item,
                        pvalue=data[meta_item]
                    ))
                    self.__meta[meta_item] = data[meta_item]

            # Then load the parameters used to check for compatibility
            # if any
            if PARAM_COMPATIBILITY_PARAMS in data:
                self.__load_compatibility_parameters(data)

            # Then load any other remaining paramaters if any and
            # merge
            if PARAM_OTHER_PARAMS in data:
                self.__load_parameters(data)

    def __load_compatibility_parameters(self, _data):
        """
        This function will load all the parameters to check for compatibility between
        the definition file and the target file. All results will be stored in the internal
        members of the object.
        :param _data: JSON-data read from the definition file.
        :return: None
        """
        assert _data is not None
        for comp_param in _data[PARAM_COMPATIBILITY_PARAMS]:
            # If all the requires properties are defined for the
            # JSON-formatted parameters, create an object otherwise
            # raise an exceptoin.
            if PARAM_NAME in comp_param and \
                    PARAM_OFFSET in comp_param and \
                    PARAM_SIZE in comp_param and \
                    PARAM_TYPE in comp_param and \
                    PARAM_COMPATIBLE_WITH in comp_param:
                pname = comp_param[PARAM_NAME]
                poffset = comp_param[PARAM_OFFSET]
                psize = comp_param[PARAM_SIZE]
                ptype = comp_param[PARAM_TYPE]
                pcompatible = comp_param[PARAM_COMPATIBLE_WITH]

                prelative = NO_VALUE
                if PARAM_RELATIVE in comp_param:
                    prelative = comp_param[PARAM_RELATIVE]

                # Create a CompatibilityParameters from the data read.
                parameter = CompatibilityParameter(
                    _name=pname,
                    _offset=poffset,
                    _size=psize,
                    _type=ptype,
                    _compatible_with=pcompatible,
                    _relative_to=prelative
                )

                # Add the new parameter to the internal dictionary.
                self.__compatibility[pname] = parameter

            else:
                raise Exception(MSG_ERROR_INCOMPLETE_PARAM)

    def __load_parameters(self, _data):
        assert _data is not None

        # Used to label parameters with no real name.
        unknown_count = 1

        # Retrieves the list of JSON-formatted parameters
        # from the JSON dictionary created.
        for param in _data[PARAM_OTHER_PARAMS]:
            # Check if the mandatory properties
            # have been defined in the definition file.
            if PARAM_NAME in param and \
                    PARAM_OFFSET in param and \
                    PARAM_SIZE in param and \
                    PARAM_TYPE in param:

                # Load the values into a Parameter object
                pname = param[PARAM_NAME].strip()
                poffset = param[PARAM_OFFSET]
                psize = param[PARAM_SIZE]
                ptype = param[PARAM_TYPE]

                # If the parameter has no name, generate an unique
                # identifier for it and use it as key.
                if pname.lower() == NAME_UNKNOWN or pname == EMPTY_STRING:
                    pname = UNKNOWN_PARAM_FORMAT.format(
                        prefix=NAME_UNKNOWN,
                        idx=unknown_count
                    )
                    unknown_count += 1

                # Get the name of the relative parameter, if any
                prelative = NO_VALUE
                if PARAM_RELATIVE in param:
                    prelative = param[PARAM_RELATIVE]

                # Get he value of the parameter, if any
                pvalue = NO_VALUE
                if PARAM_VALUE in param:
                    pvalue = param[PARAM_VALUE]

                # Create the Parameter object.
                parameter = Parameter(
                    _name=pname,
                    _offset=poffset,
                    _size=psize,
                    _type=ptype,
                    _relative_to=prelative,
                    _value=pvalue
                )

                self.__parameters[pname] = parameter
            else:
                raise Exception(MSG_ERROR_INCOMPLETE_PARAM)


class TargetFile(AbstractFile):
    """
    The TargetFile object encapsulate the binary file from which the program
    will extract data from.
    """

    def __init__(self, _file, _base=0x0):
        """
        Initializes the TargetFile object using the path to the target
        file.
        :param _file: The absolute path to the binary file to analyze.
        :param _base: Base address from which the analysis will start.
        """
        super().__init__(_file)
        assert 0 <= _base < self.size()
        self.__base_offset = _base
        self.__fp = None

    def __repr__(self):
        """
        Returns a string representation of the object.
        :return: A string representatin of the object.
        """
        return TARGET_FILE_REPR.format(f=self.file)

    def __str__(self):
        """
        Returns the path of the target file.
        :return: The path of the target file.
        """
        return self.file

    def sha1(self):
        """
        Calculates the SHA1 hash of the file.
        :return: A string with the hex digest of the file.
        """
        self.open()
        sha1 = hashlib.sha1()
        sha1.update(self.__fp.read())
        self.close()
        return sha1.hexdigest()

    def open(self):
        """
        Opens the target file for reading.
        :return: None
        """
        self.__fp = open(self.file, "rb")

    def size(self):
        """
        Returns the size of the file in bytes.
        :return: The size of the file in bytes.
        """
        return os.path.getsize(self.file)

    def read(self, _parameter, _absolute_offset=None):
        """
        Reads the given parameter from the target file.

        :param _parameter: A Parameter object
        :param _absolute_offset The absolute offset of the parameter in the file.
        :return: The value read from the file.
        """
        assert isinstance(_parameter, Parameter)
        offset = _absolute_offset
        if offset is None:
            offset = _parameter.offset
        size = _parameter.size
        # Reads the value using the offset and size of the parameter.
        value = self.__read_at(offset, size)

        # Converts the bytes read to the proper type. If the value
        # is None, we assume an error occurred.
        if value is None:
            raise Exception(MSG_ERROR_READ_PARAM.format(
                param=str(_parameter)
            ))
        else:
            # Convert string values
            if _parameter.type in TYPE_STRING:
                value = value.decode(_parameter.type).strip()
            # Convert numeric values.
            else:
                value = struct.unpack(_parameter.type, value)[0]

        return value

    def __read_at(self, _offset, _size):
        """
        Reads bytes from the target file.
        :param _offset: The starting position to read.
        :param _size: The number of bytes to read
        :return: The bytes read from the file.
        """
        assert 0 <= _offset + _size <= self.size()

        if self.__fp is None:
            self.open()

        self.__fp.seek(_offset)
        b = self.__fp.read(_size)
        return b

    def close(self):
        """
        Closes the file if it was opened.
        :return: None
        """
        if self.__fp is not None:
            self.__fp.close()
