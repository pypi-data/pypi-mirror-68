#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

import os
#cmake start
__import__('cmake')
from cmake import CMakeExtension, CMakeBuild
#cmake end

from setuptools import setup, Extension
import site

setup( use_scm_version=True,
       packages=_packages,
       data_files=[(str(site.getusersitepackages()),['stopeight.pth'])],#required by stopeight-clibs if enabled in CMakeLists.txt
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools_scm',
           ],
       zip_safe=False,
#pip start - not in cmake_examples
       install_requires=[
          'numpy<1.17.0',#python2
          'future',
          'funcsigs',
          'matplotlib<3.0',#python2
          'PyQt5<5.11.0',# <5.11.0, because pip>=19.3 #not for python2
          ],
#pip end - not in cmake_examples
#cmake start
       ext_modules=[CMakeExtension('stopeight.matrix',libraries=['stopeight-clibs-matrix']),CMakeExtension('stopeight.grapher',libraries=['stopeight-clibs-grapher']),CMakeExtension('stopeight.analyzer',libraries=['stopeight-clibs-analyzer']),CMakeExtension('stopeight.legacy',libraries=['stopeight-clibs-legacy'])],
       cmdclass=dict(build_ext=CMakeBuild),
#cmake end
)
