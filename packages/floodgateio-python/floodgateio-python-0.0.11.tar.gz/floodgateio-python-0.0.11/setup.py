
import os
import sys
import setuptools
import unittest

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))


class SetupCommand(setuptools.Command):
    
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class PyLintCommand(SetupCommand):

    def run(self):       
        import pylint.lint 
        pylint.lint.Run([
            '--rcfile={}/tests/.pylintrc'.format(PROJECT_ROOT),
            os.path.join(PROJECT_ROOT, 'src')
            ])

class MypyCommand(SetupCommand):

    def run(self):      
        import mypy
        import mypy.main  
        mypy.main.main(None, sys.stdout, sys.stderr, [
            '--config-file={}/tests/mypy.ini'.format(PROJECT_ROOT),
            os.path.join(PROJECT_ROOT, 'src')
            ])


class TestCommand(SetupCommand):

    def run(self):        
        test_loader = unittest.TestLoader()
        suite = test_loader.discover(os.path.join(PROJECT_ROOT, 'tests'), pattern='test_*.py')
        runner = unittest.TextTestRunner()
        runner.run(suite)


def get_version():
    version = {}
    with open(os.path.join(PROJECT_ROOT, "src/floodgateio/version.py")) as fp:
        exec(fp.read(), version)
    return version['__version__']


def get_long_description():
    with open(os.path.join(PROJECT_ROOT, 'README.md'), encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name = 'floodgateio-python',
    url='https://github.com/densolo/floodgateio-python',

    description = 'floodgate.io python client',
    long_description = get_long_description(),
    long_description_content_type="text/markdown",

    version = get_version(),
    license='MIT',

    author = 'denissolo',
    
    packages = setuptools.find_packages(where='src'),
    package_dir = {'': 'src'},

    install_requires = [
        'aiohttp',
        'requests'
    ],
    
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',

    cmdclass={
        'pylint': PyLintCommand,
        'mypy': MypyCommand,
        'test': TestCommand
    },
)
