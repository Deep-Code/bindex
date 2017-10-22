#!/usr/bin/env python
# coding: utf-8
"""
    bindex.extractor
    ~~~~~~~~~~~~~

    The extractor module contains the engine of the application, which is
    responsible to take in the target file, the definition file and outputting
    the extracted data.

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

__author__ = metadata.authors[0]
__copyright__ = metadata.copyright
__version__ = metadata.version
__license__ = metadata.license
__credits__ = metadata.authors
__maintainer__ = metadata.authors[0]
__email__ = metadata.emails[0]
__status__ = metadata.status

logger = logging.getLogger(__name__)


class Extractor():
    def __init__(self, _target_file, _definition_file):
        """
        Initiates an Extractor object using the given definition and target files.

        This function does not initiate the extraction process. It merely creates
        a TargetFile object and a DefinitionFile object, which validates some variables.

        :param _target_file: The path to the target file.
        :param _definition_file: The path to the definition file.
        """
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
        """
        Verifies if the definition file given to the extractor is compatible
        with the target file.

        This function will read the parameters in the "compatibility" section
        of the definition file and extract the values of these parameters. It will
        then compare the values extracted with the values defined in the "compatible_with"
        property.

        :return: True if all the values extracted are compatible with the definition file,
        False otherwise.
        """
        parameters = self.__definition.compatibility

        for parameter_name in parameters:
            try:
                # Obtain the parameter object from the compatibility parameters.
                parameter = parameters[parameter_name]
                # Calculates the absolute offset of the parameter within the target file.
                absolute_offset = self.__get_absolute_offset(parameter)
                # Reads the value at the given offset.
                value = self.__target.read(parameter, absolute_offset)
                # Check if the value is compatible with the definition file
                if not parameter.is_compatible(value):
                    logger.error(MSG_ERROR_PARAM_NOT_COMPATIBLE.format(
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
        now_date = datetime.date.today().strftime(RESULT_DATE_FMT)
        now_time = datetime.time().strftime(RESULT_TIME_FMT)
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
                    logger.error(MSG_ERROR_FAILED_READ_PARAM.format(
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
