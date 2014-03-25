#! /usr/bin/env python
# coding: utf-8

from setuptools import setup, Command, Extension
from setuptools.command.install import install
from distutils.util import get_platform
from distutils.dist import Distribution

import subprocess
import glob
import sys


def get_host_platform():
    if sys.platform.startswith('linux'):
        return 'linux64' if sys.maxsize > 2 ** 32 else 'linux'
    elif sys.platform.startswith('win'):
        return 'win32'
    elif sys.platform.startswith('darwin'):
        return 'mac64' if sys.maxsize > 2 ** 32 else 'mac' 
    raise OSError("Unsupported host platform")


class build_extensions_with_waf(Command):
    user_options = [(
                        'use-prebuilt-libs', None,
                        'link using the prebuilt static libraries'
                    ),(
                        'debug', 'g',
                        'compile with debug config'
                    ),(
                        'platform=', 'p',
                        'target platform to build'
                    )]
    boolean_options = ['use-prebuilt-libs', 'debug']

    def initialize_options(self):
        self.use_prebuilt_libs = True
        self.debug = None
        self.platform = None

    def finalize_options(self):
        if self.platform is None:
            self.platform = get_host_platform()
        self.plat_name = get_platform()

    def run(self):
        options = ['--platform=%s' % self.platform,
                    '--install-path=./flappy']
        if self.debug:
            options += ['--debug']
        if self.use_prebuilt_libs:
            options += ['--use-prebuilt-libs']

        subprocess.check_call(['python', 'waf', 'configure'] + options)
        subprocess.check_call(['python', 'waf', 'build'])
        subprocess.check_call(['python', 'waf', 'install'])


class flappy_install(install):
    def run(self):
        self.run_command("build_extensions_with_waf")
        install.run(self)

class flappy_dist(Distribution):
    def has_ext_modules(self):
        return True

sys.path.append('./flappy')
from __version__ import VERSION

readme = open('./README.rst', 'r').read()

setup(  name='Flappy',
        version=VERSION,
        description='Multimedia library with the Adobe Flash-like API',
        long_description=readme,
        author='Michael P.',
        author_email='pyronimous@gmail.com',
        url='https://github.com/pyronimous/flappy',
        license='MIT',
        distclass=flappy_dist,
        cmdclass={ 
            'build_extensions_with_waf' : build_extensions_with_waf,
            'install' : flappy_install,
        },
        packages=[
            'flappy',
            'flappy.display',
            'flappy.display3d',
            'flappy.events',
            'flappy.geom',
            'flappy.text',
            'flappy.filters',
            'flappy.ui',
        ],
        package_data={'flappy' : ['*.so', '*.pyd','*.dll']},
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Topic :: Multimedia :: Graphics',
            'Topic :: Games/Entertainment',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
