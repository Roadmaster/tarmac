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

'''Tarmac plugin for running tests pre-commit.'''
from bzrlib.lazy_import import lazy_import
lazy_import(globals(), '''
    import os
    import subprocess

    from bzrlib.errors import TipChangeRejected
    ''')

from tarmac.hooks import tarmac_hooks
from tarmac.plugins import TarmacPlugin

class Command(TarmacPlugin):
    '''Tarmac plugin for running a test command.

    This plugin checks for a config setting specific to the project.  If it
    finds one, it will run that command pre-commit.  On fail, it calls the
    do_failed method, and on success, continues.
    '''

    def run(self, command, target, source, proposal):
        try:
            self.verify_command = target.config.verify_command
        except AttributeError:
            # This can be killed two versions after 0.4, whatever version that
            # is.
            try:
                self.verify_command = target.config.test_command
                self.logger.warn(
                    'test_command config setting is deprecated. '
                    'Please use verify_command instead.')
            except AttributeError:
                return

        self.proposal = proposal

        cwd = os.getcwd()
        os.chdir(target.config.tree_dir)
        self.logger.debug('Running test command: %s' % self.verify_command)
        proc = subprocess.Popen(
            self.verify_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        self.logger.debug('Completed test command: %s' % self.verify_command)
        stdout_value, stderr_value = proc.communicate()
        return_code = proc.wait()
        os.chdir(cwd)

        if return_code != 0:
            self.do_failed(stdout_value, stderr_value)

    def do_failed(self, stdout_value, stderr_value):
        '''Perform failure tests.

        In this case, the output of the test command is posted as a comment,
        and the merge proposal is then set to "Needs review" so that Tarmac
        doesn't attempt to merge it again without human interaction.  An
        exception is then raised to prevent the commit from happening.
        '''
        self.logger.warn(u'Test command "%s" failed.' % self.verify_command)
        comment = (u'The attempt to merge %(source)s into %(target)s failed.' +
                   u'Below is the output from the failed tests.\n\n' +
                   u'%(output)s') % {
            'source' : self.proposal.source_branch.display_name,
            'target' : self.proposal.target_branch.display_name,
            'output' : u'\n'.join([stdout_value, stderr_value]),
            }
        raise TipChangeRejected(comment)


tarmac_hooks['tarmac_pre_commit'].hook(Command(), 'Command plugin')
