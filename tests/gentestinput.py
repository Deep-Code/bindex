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
import struct

test_file = ".\\input.bin"
fp = open(test_file, "wb")
fp.write("DeepCode  ".encode("ascii"))
fp.write("1.09.145".encode("utf-16"))
fp.write(struct.pack("I", 0xFFFFAA))
tp2 = "Test Comment Parameter"
fp.write(tp2.encode("utf-8"))
fp.write(b'\x00\x00')
fp.close()
