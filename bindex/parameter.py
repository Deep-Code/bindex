#!/usr/bin/env python
# coding: utf-8
"""
    bindex.parameter
    ~~~~~~~~~~~~~

    A description which can be long and explain the complete
    functionality of this module even with indented code examples.
    Class/Function however should not be documented here.

    :copyright: 2017, Jonathan Racicot, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import json

from bindex.const import *

__author__ = metadata.authors[0]
__copyright__ = metadata.copyright
__version__ = metadata.version
__license__ = metadata.license
__credits__ = metadata.authors
__maintainer__ = metadata.authors[0]
__email__ = metadata.emails[0]
__status__ = metadata.status


class Parameter(object):
    """
    The Parameter object describe a data item to extract from the targeted file.
    The object holds all the information required to extract and store the value extracted
    from the given file.
    """

    def __init__(self, _name, _offset, _size, _type, _relative_to=NO_VALUE, _value=NO_VALUE):
        """
        Initializes a new Parameter object using the provided parameters.

        :param _name: The name of the parameter.
        :param _offset: The absolute or relative address of the parameter in the
        targeted file.
        :param _size: The number of bytes to read in the target file.
        :param _relative_to: The name of the parameter from which the given offset
        is calculated. Can be None.
        :param _value: The initial value of the parameter. Can be None.
        :param _type: The string encoding or struct format to use when unpacking
        the bytes of the parameter.
        """
        assert _name is not None and len(_name.strip()) > 0
        assert _size > 0
        assert isinstance(_offset, int) and _offset >= 0

        self.__name = _name
        self.__offset = _offset
        self.__relative_to = _relative_to
        self.__size = _size
        self.update(_value)
        self.__type = _type

    def __repr__(self):
        """
        Returns a string representation of the Parameter object as formatted by
        bindex.const.PARAMETER_REPR.
        :return: A string representation of the Parameter object.
        """
        s = PARAMETER_REPR.format(
            n=self.name,
            sz=self.size,
            off=self.offset,
            type=str(self.type),
            rn=str(self.relative_to),
            val=str(self.value)
        )
        return s

    def __str__(self):
        """
        Returns a string representation of the Parameter object as formated by
        bindex.const.PARAMETER_STR.
        :return: A string representation of the Parameter object.
        """
        s = PARAMETER_STR.format(
            pn=self.name,
            sz=self.size,
            off=self.offset,
            type=self.type,
            rn=self.relative_to
        )
        return s

    @property
    def name(self):
        """
        Returns the name of the parameter.
        :return: The name of the parameter.
        """
        return self.__name

    @property
    def size(self):
        """
        Returns the size in bytes of the parameter.
        :return: The size in bytes of the parameter.
        """
        return self.__size

    @property
    def offset(self):
        """
        Returns the offset of the parameter within the target file.
        :return: The offset of the parameter within the target file.
        """
        return self.__offset

    def update_offset(self, _offset):
        self.__offset = _offset

    @property
    def type(self):
        """
        Returns the type of the parameter.

        The type can be either a string encoding or a format string
        to pass to a struct.unpack method.

        :return: The type of the parameter.
        """
        return self.__type

    @property
    def relative_to(self):
        """
        Returns the name of the parameter to which this Parameter
         object is related to.
        :return: The name of the related Parameter object.
        """
        return self.__relative_to

    @property
    def value(self):
        """
        Returns the value of the parameter.

        If a value was assigned to this parameter, the function will return
        its value, otherwise returns None.

        :return: The value of the parameter.
        """
        return self.__value

    def update(self, _value):
        """
        Replaces the value of the parameter with the given value/
        :param _value: The new value of the parameter.
        :return: None
        """
        self.__value = _value


class CompatibilityParameter(Parameter):
    """
    This object is an extension of the Parameter class and is used
    to define parameters used to validate the compatibility of the
    target file.
    """

    def __init__(self, _name, _offset, _size, _type, _compatible_with, _relative_to=NO_VALUE, _value=NO_VALUE):
        """
        Initializes a new Parameter object using the provided parameters.

        :param _name: The name of the parameter.
        :param _offset: The absolute or relative address of the parameter in the
        targeted file.
        :param _size: The number of bytes to read in the target file.
        :param _relative_to: The name of the parameter from which the given offset
        is calculated. Can be None.
        :param _compatible_with A list of compatible values
        :param _value: The initial value of the parameter. Can be None.
        :param _type: The string encoding or struct format to use when unpacking
        the bytes of the parameter.
        """
        super().__init__(
            _name=_name,
            _offset=_offset,
            _size=_size,
            _type=_type,
            _relative_to=_relative_to,
            _value=_value
        )
        assert _compatible_with is not None
        self.__compatible_with = _compatible_with

    @property
    def compatible_with_list(self):
        """
        Returns the list of compatible values for this parameter.
        :return: List of compatible values for this parameter.
        """
        return self.__compatible_with

    def is_compatible(self, _value):
        """
        Verifies if the value is compatible with the parameter.
        :param _value: The value to verify.
        :return: True if the value is in the list of compatible values,
        False otherwise.
        """
        return _value in self.__compatible_with


class ParameterJsonEncoder(json.JSONEncoder):
    """
    Object used to encode a Parameter object into a JSON-formatted string.
    """

    def default(self, o):
        assert isinstance(o, Parameter)
        return {
            PARAM_NAME: o.name,
            PARAM_OFFSET: o.offset,
            PARAM_SIZE: o.size,
            PARAM_RELATIVE: o.relative_to,
            PARAM_VALUE: o.value
        }
