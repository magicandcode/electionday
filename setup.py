import os
import pathlib
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def custom_run(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        orig_run(self)
        exec(open(pathlib.Path('./setup_db.py'), encoding='utf-8').read(),
             globals())
    command_subclass.run = modified_run
    return command_subclass


@custom_run
class CustomDevelopCommand(develop):
    pass

@custom_run
class CustomInstallCommand(install):
    pass


APP_NAME, APP_SLUG = 'ElectionDay', 'electionday'

with open('./requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [req.strip() for req in f]

setup(
    name=APP_NAME,
    py_modules=[APP_SLUG],
    cmdclass={'install': CustomInstallCommand, 'develop': CustomDevelopCommand}
    install_requires=requirements,
    entry_points=f'''
        [console_scripts]
        {APP_SLUG}={APP_SLUG}:main
    ''',
)
