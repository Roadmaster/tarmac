# Copyright 2009 Paul Hummer - See LICENSE
'''Tarmac plugin for running tests pre-commit.'''
import os

from tarmac.hooks import tarmac_hooks
from tarmac.plugins import TarmacPlugin


class RunTest(TarmacPlugin):
    '''Tarmac plugin for running a test command.

    This plugin checks for a config setting specific to the project.  If it
    finds one, it will run that command pre-commit.  On fail, it calls the
    do_failed method, and on success, continues.
    '''
    #TODO: Add the specific config it checks for.
    #TODO: Add the ability to override the test command in the command line.

    def __call__(self, options, configuration, candidate, temp_dir):

        if options.test_command:
            self.test_command = options.test_command
        elif configuration.test_command:
            self.test_command = configuration.test_command
        else:
            return

        self.candidate = candidate

        cwd = os.getcwd()
        os.chdir(temp_dir)
        proc = subprocess.Popen(
            self.test_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout_value, stderr_value = proc.communicate()
        return_code = proc.wait()
        os.chdir(cwd)

        if retcode == 0:
            return

        else:
            self.do_failed(stdout_value, stderr_value)
            raise HookFailed('runtest hook failed')

    def do_failed(self):
        '''Perform failure tests.

        In this case, the output of the test command is posted as a comment,
        and the merge proposal is then set to "Needs review" so that Tarmac
        doesn't attempt to merge it again without human interaction.  An
        exception is then raised to prevent the commit from happening.
        '''
        comment = u'\n'.join([stdout_value, stderr_value])
        self.candidate.createComment(subject="Failed test command",
                                content=comment)
        self.candidate.queue_status = u'Needs review'
        self.candidate.lp_save()


tarmac_hooks['pre_tarmac_commit'].hook(RunTest(), 'Test run hook')