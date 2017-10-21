#!/usr/bin/env python
# coding: utf-8
"""
    package.module
    ~~~~~~~~~~~~~

    A description which can be long and explain the complete
    functionality of this module even with indented code examples.
    Class/Function however should not be documented here.

    :copyright: 2017, Jonathan Racicot, see AUTHORS for more details
    :license: MIT, see LICENSE for more details
"""
import unittest

from bindex.files import TargetFile
from bindex.parameter import CompatibilityParameter


class TestMain(unittest.TestCase):
    def test_create_target_file(self):
        test_file = "input.bin"
        tf = TargetFile(test_file)
        assert tf.file == test_file

    def test_read_parameter_target_file(self):
        test_file = "input.bin"
        tf = TargetFile(test_file)

        cvalue = "DeepCode"

        param = CompatibilityParameter(
            _name="manufacturer",
            _offset=0,
            _size=10,
            _type="ascii",
            _compatible_with=["ShallwCode", "DeepCode"]
        )
        pvalue = tf.read(param)
        assert cvalue == pvalue
        tf.close()
