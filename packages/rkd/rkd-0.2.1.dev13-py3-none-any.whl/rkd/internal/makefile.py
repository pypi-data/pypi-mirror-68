#
# Base RKD Makefile, contains basic commands such as :tasks, :clean or :version
#

from rkd.syntax import TaskDeclaration
from rkd.standardlib.shell import ShellCommand, ExecProcessCommand
from rkd.standardlib import InitTask, TasksListingTask, VersionTask, CreateStructureTask


IMPORTS = [
    TaskDeclaration(ShellCommand()),
    TaskDeclaration(ExecProcessCommand()),
    TaskDeclaration(InitTask()),
    TaskDeclaration(TasksListingTask()),
    TaskDeclaration(VersionTask()),
    TaskDeclaration(CreateStructureTask())
]

TASKS = [
    # example:
    # TaskAliasDeclaration(':env:test', [':py:publish', '--username=...', '--password=...'], env={'DB_PASSWORD': '123'})
]
