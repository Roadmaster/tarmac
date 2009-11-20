# Copyright 2009 Paul Hummer
# This file is part of Tarmac.
#
# Tarmac is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by
# the Free Software Foundation.
#
# Tarmac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tarmac.  If not, see <http://www.gnu.org/licenses/>.

'''Tests for Tarmac scripts.'''
# pylint: disable-msg=W0212,W0223
__metaclass__ = type

import commands
from optparse import OptionParser
import sys
import unittest

from tarmac.bin import TarmacLander, TarmacScript


class TestTarmacScript(unittest.TestCase):
    '''Tests for tarmac.bin.TarmacScript.'''

    class TarmacDummyScript(TarmacScript):
        '''A dummy Tarmac script for testability.'''
        def _create_option_parser(self):
            return OptionParser()

    def test_create_option_parser_not_implemented(self):
        '''Test that the _create_config_parser method raises NotImplemented.'''
        self.assertRaises(NotImplementedError, TarmacScript, test_mode=True)

    def test_dummy_script_option_parser(self):
        '''Test that _create_config_parser is implemented in TarmacDummyScript.
        '''
        sys.argv = ['']
        script = self.TarmacDummyScript(test_mode=True)
        self.assertTrue(isinstance(script, self.TarmacDummyScript))


class TestTarmacLander(unittest.TestCase):
    '''Tests for TarmacLander.'''

    def test_lander_dry_run(self):
        '''Test that setting --dry-run sets the dry_run property.'''
        sys.argv = ['', 'foo', '--dry-run']
        script = TarmacLander(test_mode=True)
        self.assertTrue(script.dry_run)

    def test_lander_project(self):
        '''Test that the project argument gets handled properly.'''
        sys.argv = ['', 'foo']
        script = TarmacLander(test_mode=True)
        self.assertEqual(script.project, u'foo')

    def test_test_mode(self):
        '''Test that test_mode is set correctly.'''
        script = TarmacLander(test_mode=True)
        self.assertTrue(script.test_mode)


class TestTarmacScript(unittest.TestCase):
    '''Tests for tarmac-script.'''

    def test_script(self):
        status, output = commands.getstatusoutput('../tarmac-script')
        self.assertEqual(output, '')
