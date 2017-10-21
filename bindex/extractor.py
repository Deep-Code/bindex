#!/usr/bin/env python
# coding: utf-8
"""
    bindex.extractor
    ~~~~~~~~~~~~~

    A description which can be long and explain the complete
    functionality of this module even with indented code examples.
    Class/Function however should not be documented here.

    :copyright: 2017, Jonathan Racicot, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import datetime
import logging
import os

from bindex.const import *
from bindex.files import DefinitionFile
from bindex.files import TargetFile
from bindex.parameter import Parameter

logger = logging.getLogger(__name__)


class Extractor():
    def __init__(self, _target_file, _definition_file):
        assert os.path.isfile(_target_file)
        assert os.path.isfile(_definition_file)

        self.__target = TargetFile(_target_file)
        self.__definition = DefinitionFile(_definition_file)
        self.__extracted_data = {}

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return EXTRACTOR_REPR.format(
            df=str(self.definition),
            tf=str(self.target)
        )

    @property
    def definition(self):
        """
        Returns the path of the definition file used by the extractor.
        :return: The path of the definition file used by the extractor.
        """
        return str(self.__definition)

    @property
    def target(self):
        """
        Returns the path of the target file being analyzed by the extractor.
        :return: The path of the target file being analyzed by the extractor.
        """
        return str(self.__target)

    def is_compatible(self):
        parameters = self.__definition.compatibility
        for parameter_name in parameters:
            try:
                parameter = parameters[parameter_name]
                absolute_offset = self.__get_absolute_offset(parameter)
                value = self.__target.read(parameter, absolute_offset)
                if not parameter.is_compatible(value):
                    logger.error("Parameter '{param:s}' is not compatible with target file:".format(
                        param=parameter_name))
                    logger.error("\tValue from target: {vt:s}.".format(vt=str(value)))
                    logger.error("\tCompatible with: {valid:s}.".format(
                        valid=', '.join(parameter.compatible_with_list)))
                    return False
            except Exception as e:
                logger.error(str(e))
                return False

        return True

    def extract(self):
        """
        Extract the parameters defined in the definition file from the provided
        target file.
        :return: A dictionary containing metadata and the values extracted.
        """
        assert self.__target is not None
        assert self.__definition is not None

        # The values dictionary will contain the parameters extracted
        # from the file.
        values = {}
        # Initiate the result dictionary with metadata to identify
        # the analysis.
        now_date = datetime.date.today().strftime("%Y.%m.%d")
        now_time = datetime.time().strftime("%H.%M.%S")
        result = {
            PARAM_METADATA: {
                PARAM_DEF_FILE: self.definition,
                PARAM_ORIGINAL_FILE: self.target,
                PARAM_ANALYSIS_DATE: DATETIME_STAMP.format(
                    cdate=now_date,
                    ctime=now_time
                ),
                PARAM_ORIGINAL_FILE_HASH: self.__target.sha1()
            }
        }

        # Open the target file for reading. Don't forget to close it
        # at the end.
        self.__target.open()

        # Check for compatibility between the target and definition
        # files.
        if self.is_compatible():
            # Start iterating the Parameters objects to extract them.
            parameters = self.__definition.parameters
            for parameter_name in parameters.keys():
                parameter = parameters[parameter_name]
                try:
                    # Calculate the real offset of the parameter
                    absolute_offset = self.__get_absolute_offset(parameter)
                    # Read the value from the file
                    value = self.__target.read(parameter, absolute_offset)
                    logger.debug("{param:<16s}:{val:s}".format(
                        param=parameter_name,
                        val=str(value)
                    ))
                except Exception as e:
                    value = ERROR_VALUE
                    logger.error("Failed to extract parameter '{param:s}': {err:s}".format(
                        param=str(parameter),
                        err=str(e)))
                # Store the result into the values parameter.
                values[parameter.name] = value
        else:
            logger.error(MSG_ERROR_NOT_COMPATIBLE)
            raise Exception(MSG_ERROR_NOT_COMPATIBLE)

        # Add the extracted parameters to the results dictionary
        result[PARAM_OTHER_PARAMS] = values
        # Close the target file.
        self.__target.close()

        return result

    def __get_absolute_offset(self, _parameter):
        """
        Calculates the absolute offset of the parameter from the parameters
        related.

        :param _parameter: The Parameter from which to calculate the absolute offset.
        :return: The absolute offset of the parameter.
        """
        assert isinstance(_parameter, Parameter)

        if _parameter.relative_to is None:
            return _parameter.offset
        else:
            related_param = self.__definition.related(_parameter)
            return _parameter.offset + self.__get_absolute_offset(related_param) + related_param.size

    def extract_to_file(self, _output_file):
        import json
        assert _output_file is not None
        results = self.extract()

        if results is not None and len(results) > 0:
            with open(_output_file, "w") as fp:
                json.dump(fp, results)
        else:
            logging.warning(MSG_ERROR_NO_DATA_EXTRACTED.format(f=self.__target.file))
