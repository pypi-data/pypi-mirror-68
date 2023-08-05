#!/usr/bin/env python

_packages = [ 'stopeight','stopeight.logging','stopeight.comparator','stopeight.multiprocessing','stopeight.util','stopeight.util.editor','stopeight.util.editor.modules']

import os
#distutils start
__import__('python')
from python import get_pybind_include, BuildExt
_include_dirs=[
    os.path.join('stopeight-clibs','cmake-git-version-tracking','better-example'),
    # Path to pybind11 headers
    str(get_pybind_include()),
    str(get_pybind_include(user=True)),
]
_qt5_include_dirs=_include_dirs
_library_dirs=[]
#distutils end

from setuptools import setup, Extension

setup( name='stopeight',
       version='0.2.19',
       description='stopeight: Comparing sequences of points in 2 dimensions',
       long_description='stopeight: Comparing sequences of points in 2 dimensions by visually overlapping them using matrix transformations (translation, scaling and rotation) and getting a boolean result.',
       author='Fassio Blatter',
       author_email='fassio@specpose.com',
       license='GNU General Public License, version 2',
       url='https://github.com/specpose/stopeight',
       python_requires='>=2.7',
       classifiers=[
           "Development Status :: 3 - Alpha",
           "Intended Audience :: Developers",
           "Topic :: Multimedia :: Sound/Audio :: Analysis",
           "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
           "Programming Language :: Python :: 2.7",
           ],
       keywords="signal-analysis pen-stroke",
       packages=_packages,
       entry_points={
           'setuptools.installation':['eggsecutable = stopeight.util.editor.dispatch:main_func',]
           },
       setup_requires=[
           'setuptools',
           'pybind11>=2.4',
           'setuptools_scm',
           ],
       zip_safe=False,
#distutils start
#pip start
       install_requires=[
          'numpy<1.17.0',#python2
          'future',
          'funcsigs',
          'matplotlib<3.0',#python2
          'pybind11>=2.4',
#          'PyQt5<5.11.0',# <5.11.0, because pip>=19.3 #not for python2
          ],
#pip end
       ext_modules = [
           Extension(
               'stopeight.grapher',
               [os.path.join('stopeight-clibs','grapher-wrappers','IFPyGrapher.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','grapher')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-grapher'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.matrix',
               [os.path.join('stopeight-clibs','matrix-wrappers','IFPyMatrix.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','matrix')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=True
           ),
           Extension(
               'stopeight.analyzer',
               [os.path.join('stopeight-clibs','analyzer-wrappers','IFPyAnalyzer.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','analyzer')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
           Extension(
              'stopeight.legacy',
               [os.path.join('stopeight-clibs','legacy-wrappers','interfacepython.cpp')],
               include_dirs=_qt5_include_dirs + [
                   os.path.join('stopeight-clibs','legacy/include')
               ],
               library_dirs=_library_dirs,
               libraries=['stopeight-clibs-legacy','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
       ],
       cmdclass={'build_ext': BuildExt},
#distutils end
)
