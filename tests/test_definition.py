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
from bindex.files import DefinitionFile


class TestMain(unittest.TestCase):
    def test_create_definition_file(self):
        test_file = "test.config"
        definition_file = DefinitionFile(test_file)
        assert definition_file.file == test_file

    def test_load_definition_file_params(self):
        test_file = "test.config"
        pn1 = "TestParam1"
        po1 = 0
        ps1 = 4
        pt1 = "I"
        pv1 = NO_VALUE
        pr1 = "version"

        pn2 = "TestParam2"
        po2 = 0
        ps2 = 24
        pt2 = "utf-8"
        pv2 = 0
        pr2 = pn1

        definition_file = DefinitionFile(test_file)
        params = definition_file.parameters
        assert len(params) == 2
        assert pn1 in params
        assert pn2 in params

        p1 = params[pn1]
        assert p1.name == pn1
        assert p1.offset == po1
        assert p1.size == ps1
        assert p1.type == pt1
        assert p1.value == pv1
        assert p1.relative_to == pr1

        p2 = params[pn2]
        assert p2.name == pn2
        assert p2.offset == po2
        assert p2.size == ps2
        assert p2.type == pt2
        assert p2.value == pv2
        assert p2.relative_to == pr2

    def test_load_definition_file_comp_params(self):
        test_file = "test.config"
        pn1 = "manufacturer"
        po1 = 0
        ps1 = 10
        pt1 = "ascii"
        pcw1 = ["ShallwCode", "DeepCode"]
        pr1 = NO_VALUE

        pn2 = "version"
        po2 = 2
        ps2 = 16
        pt2 = "utf-16"
        pcw2 = ["1.08.100", "1.09.145", "1.10.748"]
        pr2 = pn1

        definition_file = DefinitionFile(test_file)
        params = definition_file.compatibility
        assert len(params) == 2
        assert pn1 in params
        assert pn2 in params

        p1 = params[pn1]
        assert p1.name == pn1
        assert p1.offset == po1
        assert p1.size == ps1
        assert p1.type == pt1
        assert p1.compatible_with_list == pcw1
        assert p1.relative_to == pr1

        p2 = params[pn2]
        assert p2.name == pn2
        assert p2.offset == po2
        assert p2.size == ps2
        assert p2.type == pt2
        assert p2.compatible_with_list == pcw2
        assert p2.relative_to == pr2

    def test_is_compatible_with_comp_param(self):
        test_file = "test.config"
        pn2 = "version"
        vcomp = "1.09.145"

        definition_file = DefinitionFile(test_file)
        params = definition_file.compatibility
        assert pn2 in params
        pa = params[pn2]
        # pcw2 = ["1.08.100", "1.09.145", "1.10.748"]
        assert pa.is_compatible(vcomp)

    def test_is_not_compatible_with_comp_param(self):
        test_file = "test.config"
        pn2 = "version"
        vcomp = "1.10.001"

        definition_file = DefinitionFile(test_file)
        params = definition_file.compatibility
        assert pn2 in params
        pa = params[pn2]
        # pcw2 = ["1.08.100", "1.09.145", "1.10.748"]
        assert not pa.is_compatible(vcomp)

    def test_related_parameter(self):
        test_file = "test.config"
        pname = "version"
        definition_file = DefinitionFile(test_file)
        assert pname in definition_file.compatibility.keys()
        param = definition_file.compatibility[pname]
        parent = definition_file.related(param)
        assert parent is not None
        assert parent.name == "manufacturer"

    def test_no_related_parameter(self):
        test_file = "test.config"
        pname = "manufacturer"
        definition_file = DefinitionFile(test_file)
        assert pname in definition_file.compatibility.keys()
        param = definition_file.compatibility[pname]
        parent = definition_file.related(param)
        assert parent is None
