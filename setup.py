import os
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def custom_run(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        orig_run(self)
        # Database setup after package installation.
        exec(open('setup_db.py').read(), globals())
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

with open('./requirements-dev.txt', 'r', encoding='utf-8') as f:
    requirements_dev = [req.strip() for req in f]

setup(
    name=APP_NAME,
    py_modules=[APP_SLUG],
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },
    install_requires=requirements,
    develop_requires=requirements_dev,
    entry_points=f'''
        [console_scripts]
        {APP_SLUG}={APP_SLUG}:main
    ''',
)
