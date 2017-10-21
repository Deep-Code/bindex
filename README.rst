====================================
Bindex - Binary Data Extraction Tool
====================================

.. image:: https://travis-ci.org/seanfisk/python-project-template.png
:target: https://travis-ci.org/seanfisk/python-project-template

This application is designed to extract binary data from various types of binary files based on rules defined in
a definition file. The objective of Bindex is to provide a customisable way to extract data from configuration files,
memory dumps or other files without creating a new script for each type of file analyzed. Bindex will take a
JSON-formatted file containing information on what items to extract from a target file and where to find them.

To use the script, execute the following command::

    usage

Installation
============

Using Pip
---------

Bindex can be used via the pip installer::

    pip install --upgrade-pip
    pip install bindex

Using the Setup Script
----------------------

If you don't have access to pip, simply used the install script provided with Bindex::

    python setup.py install

Usage
=====

The script provides the following options from the command-line::

        usage

Definition Files
================

Definition files are JSON-formatted files containing information on how to extract the desired data items from
binary files. These files are composed of 3 main components:

* Metadata; information about the definition file.
* Compatibility; information about the type of binary file parsed by this definition.
* Parameters; information about which parameters to extract and how.

Metadata
--------

The first items of the definition file are metadata about the definition file::

  {
      "description" : "Definition file to parse example A-01",
      "author": "Jonathan Racicot",
      "version" : "1.0",
      "creation_date" : "2017-10-10",
      ...
  }

As its name implies, the description field provide a description of the type of files this definition file
will parse. The remaining fields are self-explanatory:

* author: identity of the creator of the definition file.
* version: version of the definition file.
* creation_date: The date the file was created.

None of the metadata items are mandatory and can be omitted.

Parameters
----------

A "parameter" is the name given to a single data item to be extracted from the target file. Parameters contain the
information needed find and read a specific value in the target file::

    "parameters" : [
        {
          "name": "TestParam1",
          "offset" : 0,
          "relative_to" : "version",
          "size" : 4,
          "type" : "I"
        },
        ...
    ]

In the example above, we have the definition for a parameter called "TestParam1". The definition contains the following
information:

* name: The name of the parameter. The name should be unique for each parameter. However, if no name is given or
if named "unknown", the program will automatically give the parameter a name suffixed with a number to uniquely identify
the parameter.
* offset: The offset is the distance, in bytes, from the beginning of the file or the parameter provided in the
'relative_to' field. In the example above, the "TestParam1" parameter is immediately following the parameter "version".
* relative_to: Contains the name of a parameter preceding the current parameter from which the offset will be calculated
from. In the example above, the 'relative_to' field contains the name "version", meaning that "TestParam1" is following
the "version" parameter (offset is 0).
* size: Specifies the number of bytes to read from the target file.
* type: the value of the type field will be used to convert the bytes read from the target file to a base type: either
a string or a numeric value.

Compatibility Parameters
------------------------

The definition file may also contain a special set of parameters that will determine which kind of target files
are supported by the current definition file::

    {
    ...
        "compatibility" : [
            {
              "name" : "manufacturer",
              "offset" : 0,
              "size" : 10,
              "type": "ascii",
              "compatible_with" : [
                "ShallwCode", "DeepCode"
              ]
            },
            {
              "name": "version",
              "offset" : 2,
              "size" : 16,
              "type" : "utf-16",
              "relative_to" : "manufacturer",
              "compatible_with" : [
                "1.08.100", "1.09.145", "1.10.748"
              ]
            }
        ],
    ...
    }

The parameters defined in the compatibility segment are practically similar to the one in the parameters segment but
contains an additional field named "compatible_with". This field is an array of values for the specific field that
indicates that the target file will be properly parsed by the current definition file. If the application fails to
read the value or extracts a value for the parameters that is not in the list of compatible values, the program will
exit. In order to skip a compatibility check, simply move these parameters into the "parameters" section.

Authors
=======

.. _DeepCode: https://www.deepcode.ca
