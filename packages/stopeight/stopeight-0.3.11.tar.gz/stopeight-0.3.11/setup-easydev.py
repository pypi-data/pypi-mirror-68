#!/usr/bin/env python

_packages = ['stopeight']

import os
#cmake start
__import__('cmake')
from cmake import CMakeExtension, CMakeBuild
#cmake end

from setuptools import setup, Extension
import site

setup( use_scm_version=True,
       packages=_packages,
#      data_files=[(str(site.getusersitepackages()),['stopeight.pth'])],#required by stopeight-clibs if enabled in CMakeLists.txt
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools_scm',
           ],
       zip_safe=False,
#pip start - not in cmake_examples
       install_requires=[
          'numpy',
          'future',
          'funcsigs',
          'matplotlib',
          'PyQt5',# >5.11.0: install with pip, not easy_setup!
          ],
#pip end - not in cmake_examples
#cmake start
       ext_modules=[CMakeExtension('stopeight.matrix',libraries=['stopeight-clibs-matrix']),CMakeExtension('stopeight.grapher',libraries=['stopeight-clibs-grapher']),CMakeExtension('stopeight.analyzer',libraries=['stopeight-clibs-analyzer']),CMakeExtension('stopeight.legacy',libraries=['stopeight-clibs-legacy'])],
       cmdclass=dict(build_ext=CMakeBuild),
#cmake end
)
