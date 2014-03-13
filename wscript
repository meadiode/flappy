#! /usr/bin/env python
# encoding: utf-8

import sys
import os
import site
import waflib

sys.path.append('./flappy')
from __version__ import VERSION

top = '.' 
out = 'build'

APPNAME = 'flappy'
PACKAGE_NAME = APPNAME

PLATFORMS = ['linux', 'linux64', 'mac', 'mac64', 'win32']


def options(opt):
    opt.load(['compiler_cxx', 'compiler_c', 'python', 'cython'])
    opt.add_option('--platform', action='store', choices=PLATFORMS, 
                        help='Target platform to build')
    opt.add_option('--debug', action='store_true', default=False, 
                        help='Debug build')    
    opt.add_option('--user', action='store_true', default=False, 
                    help='Install files in the user site packages directory')    
    opt.add_option('--use-prebuilt-libs', action='store_true', default=False, 
                    help='Link using the prebuilt static libraries')    
    opt.add_option('--install-path', action='store', default=None, 
                    help='Define a custom install path')


def configure(conf):
    conf.load(['compiler_cxx', 'compiler_c', 'python', 'cython'])
    conf.check_python_version()
    conf.check_python_headers()

    if conf.options.install_path is not None:
        conf.env.INSTALL_PATH = conf.options.install_path
    else:
        if conf.options.user:
            conf.env.INSTALL_PATH = os.path.join(
                                    site.getusersitepackages(), PACKAGE_NAME)
        else:
            conf.env.INSTALL_PATH = os.path.join(
                                    site.getsitepackages()[0], PACKAGE_NAME)

    conf.env.opt_user = conf.options.user
    conf.env.opt_use_prebuilt_libs = conf.options.use_prebuilt_libs

    conf.env.CYTHON_DEFINES = {}
    
    conf.recurse('openfl_lime')
    conf.recurse('_core')
    conf.recurse('_gl')


def build(bld):
    bld.recurse('openfl_lime')
    bld.recurse('_core')
    bld.recurse('_gl')

    # flappy_dir = bld.path.find_node('flappy')
    # bld.install_files(bld.env.INSTALL_PATH, flappy_dir.ant_glob('**/*.py'),
    #                     cwd=flappy_dir, relative_trick=True)

def init(ctx):
    ctx.options.debug = bool(ctx.options.debug)
    plat = ctx.options.platform
    if not plat:
        plat = get_host_platform()
        ctx.options.platform = plat

    from waflib.Build import BuildContext, CleanContext, InstallContext, \
                                                UninstallContext, StepContext
    for ctx_class in (BuildContext, CleanContext, InstallContext, 
                                        UninstallContext, StepContext):
        var = ''
        if plat in PLATFORMS:
            var = '%s/%s' % (plat, 'debug' if ctx.options.debug else 'release')
        class tmp(ctx_class):
            variant = var

from waflib.Configure import conf

def get_host_platform():
    if sys.platform.startswith('linux'):
        return 'linux64' if sys.maxsize > 2 ** 32 else 'linux'
    elif sys.platform.startswith('win'):
        return 'win32'
    elif sys.platform.startswith('darwin'):
        return 'mac64' if sys.maxsize > 2 ** 32 else 'mac' 
    raise OSError("Unsupported host platform")

