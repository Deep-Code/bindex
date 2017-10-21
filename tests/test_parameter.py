# -*- coding: utf-8 -*-

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import unittest

from bindex.const import *
from bindex.parameter import Parameter, CompatibilityParameter


class TestMain(unittest.TestCase):
    def test_create_parameter_success(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = NO_VALUE
        ptype = "utf-8"

        param = Parameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype
        )

        assert param.name == pname
        assert param.offset == poffset
        assert param.size == psize
        assert param.relative_to == NO_VALUE
        assert param.value == NO_VALUE
        assert param.type == ptype

    def test_update_parameter_value(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = None
        ptype = "utf-8"

        new_value = 0x323232

        param = Parameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype
        )

        param.update(new_value)
        assert param.value == new_value

    def test_repr_parameter(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = None
        ptype = "utf-8"

        param = Parameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype
        )

        # "<Parameter Name='{n:s}', Offset=0x{off:08X}, Size={sz:d} byte(s), RelativeTo:{rn:s}, Type={type:s}, Value={val:s}"
        assert repr(param) == PARAMETER_REPR.format(
            n=pname,
            off=poffset,
            sz=psize,
            rn=str(prelative),
            type=ptype,
            val=str(pvalue)
        )

    def test_create_comp_param(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = None
        ptype = "utf-8"
        p_compatible_w = ["TestItemA", "TestItemB", "TestItemC"]

        param = CompatibilityParameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype,
            _compatible_with=p_compatible_w
        )

        assert param.name == pname
        assert param.offset == poffset
        assert param.size == psize
        assert param.relative_to == NO_VALUE
        assert param.value == NO_VALUE
        assert param.type == ptype
        assert param.compatible_with_list == p_compatible_w

    def test_is_compatible_comp_param(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = None
        ptype = "utf-8"
        p_compatible_w = ["TestItemA", "TestItemB", "TestItemC"]

        cvalue = "TestItemA"

        param = CompatibilityParameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype,
            _compatible_with=p_compatible_w
        )

        assert param.is_compatible(cvalue)

    def test_is_not_compatible_comp_param(self):
        pname = "TestParam"
        poffset = 0x10
        psize = 2
        prelative = NO_VALUE
        pvalue = None
        ptype = "utf-8"
        p_compatible_w = ["TestItemA", "TestItemB", "TestItemC"]

        cvalue = "TestItemX"

        param = CompatibilityParameter(
            _name=pname,
            _offset=poffset,
            _size=psize,
            _relative_to=prelative,
            _value=pvalue,
            _type=ptype,
            _compatible_with=p_compatible_w
        )

        assert not param.is_compatible(cvalue)
