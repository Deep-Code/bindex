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

from bindex.const import *
from bindex.extractor import Extractor


class TestMain(unittest.TestCase):
    def test_extractor_create(self):
        df = "test.config"
        tf = "input.bin"
        extractor = Extractor(
            _definition_file=df,
            _target_file=tf
        )

        assert extractor.definition == df
        assert extractor.target == tf

    def test_extractor_is_compatible(self):
        df = "test.config"
        tf = "input.bin"
        extractor = Extractor(
            _definition_file=df,
            _target_file=tf
        )

        assert extractor.is_compatible()

    def test_extractor_parameters(self):
        df = "test.config"
        tf = "input.bin"
        extractor = Extractor(
            _definition_file=df,
            _target_file=tf
        )
        result = extractor.extract()
        assert "TestParam1" in result[PARAM_OTHER_PARAMS].keys()
        assert "TestParam2" in result[PARAM_OTHER_PARAMS].keys()
        assert result[PARAM_OTHER_PARAMS]["TestParam1"] == 0xFFFFAA
        assert result[PARAM_OTHER_PARAMS]["TestParam2"] == "Test Comment Parameter"
