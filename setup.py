from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='synonym-extractor',
    version='0.1.6',
    url='http://github.com/vi3k6i5/synonym-extractor',
    author='Vikash Singh',
    author_email='vikash.duliajan@gmail.com',
    description='Extract synonyms from sentences using Aho Corasick algorithm',
    long_description=open('README.rst').read(),
    packages=['synonym'],
    install_requires=[],
    platforms='any',
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ]
)
