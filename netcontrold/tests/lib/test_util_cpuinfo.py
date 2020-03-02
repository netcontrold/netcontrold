#
#  Copyright (c) 2020 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from unittest import mock
from unittest import TestCase

from netcontrold.lib import util

# Create dumy file to fool function

_BASIC_CPU_INFO_Negative = """
core id 		: 0
processor		: 0
physical id     : 0
core id 		: 1
processor		: 1
physical id 	: 0
"""

_BASIC_CPU_INFO_Positive = """
processor		: 0
core id 		: 0
physical id 	: 0

processor		: 1
core id 		: 0
physical id 	: 0

processor		: 2
core id 		: 1
physical id 	: 0

processor		: 3
core id 		: 1
physical id 	: 0
"""

_BASIC_CPU_INFO_Processorid_NULL = """
processor       : 
physical id     : 0
core id         : 1
processor       : 
physical id     : 0
"""




class TestUtil(TestCase):

    @mock.patch('netcontrold.lib.util.open')
    def test_cpuinfo_Negative(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data=_BASIC_CPU_INFO_Negative).return_value
        ]
        self.assertRaises(ValueError, util.cpuinfo)


    @mock.patch('netcontrold.lib.util.open')
    def test_cpuinfo_Processorid(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data=_BASIC_CPU_INFO_Processorid_NULL).return_value
        ]
        self.assertRaises(ValueError, util.cpuinfo)
        print("Processor id can't be NULL")


    @mock.patch('netcontrold.lib.util.open')
    def test_cpuinfo_basic(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data=_BASIC_CPU_INFO_Positive).return_value
        ]
        expected = [{'processor': '0', 'core id': '0', 'physical id': '0'},
                    {'processor': '1', 'core id': '0', 'physical id': '0'},
                    {'processor': '2', 'core id': '1', 'physical id': '0'},
                    {'processor': '3', 'core id': '1', 'physical id': '0'}]
        out = util.cpuinfo()
        self.assertEqual(out, expected)

    @mock.patch('netcontrold.lib.util.open')
    def test_cpuinfo_is_empty(self, mock_open):
        mock_open.side_effect = [
            mock.mock_open(read_data="").return_value
        ]
        out = util.cpuinfo()
        expected = []
        self.assertEqual(out, expected)

    
