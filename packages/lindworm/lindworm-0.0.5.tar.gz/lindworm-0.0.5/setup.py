#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:         setup.py
# Purpose:      setup definition
#               
# Author:       Walter Obweger
#
# Created:      20191207
# CVS-ID:       $Id$
# Copyright:    (c) 2019 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import io
import os
import re
import sys
from setuptools import setup

# +++++ beg:get version number from package init
with open('lindworm/__init__.py', 'r') as oFile:
    sVersion = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        oFile.read(), re.MULTILINE).group(1)
# ----- end:get version number from package init

# +++++ beg:use readme as description
# Use the README.md content for the long description:
with io.open("lindworm/README.md", encoding="utf-8") as oFile:
    sDescLong = oFile.read()
# ----- end:use readme as description

setup(
    name='lindworm',
    version=sVersion,
    description='core tools covering folder content, markdown, GUI',
    long_description=sDescLong,
    long_description_content_type="text/markdown",
    author='Walter Obweger',
    author_email='walter.obweger@gmail.com',
    url='https://gitlab.com/wobweger/lindworm',
    project_urls={
        'Documentation': 'https://gitlab.com/wobweger/lindworm',
    },
    license='MIT',
    packages=[
        'lindworm',
        #'lindworm.pyGatherMD',
        #'lindworm.mt',
        #'lindworm.pcs7',
        #'lindworm.pd',
        #'lindworm.xd',
    ],
    test_suite='tests',
    install_requires=[
        'pandas',
        'pysimplegui',
        #'pyobjc-core;platform_system=="Darwin"', 
        #'pyobjc;platform_system=="Darwin"',
        #'python3-Xlib;platform_system=="Linux" and python_version>="3.0"', 'Xlib;platform_system=="Linux" and python_version<"3.0"',
        #'pymsgbox', 
        #'PyTweening>=1.0.1', 
        #'pyscreeze>=0.1.21', 
        #'pygetwindow>=0.0.5', 
        #'mouseinfo'
        ],
    
    keywords="tools",
    classifiers=[
        'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        #'Environment :: X11 Applications',
        #'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        #'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        #'Programming Language :: Python :: Implementation :: CPython',
        #'Programming Language :: Python :: Implementation :: PyPy',
        #'Topic :: Desktop Environment :: File Managers',
        'Topic :: Documentation',
        #'Topic :: Office/Business',
        #'Topic :: Scientific/Engineering',
        #'Topic :: Software Development',
        #'Topic :: System',
        #'Topic :: System :: Archiving',
        #'Topic :: System :: Distributed Computing',
        #'Topic :: System :: Filesystems',
        #'Topic :: System :: Operating System',
        #'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'lindworm.pyGatherMD = lindworm.pyGatherMD:main',
            'lindworm.ldmStorageFolder = lindworm.ldmStorageFolder:main',
        ],
        'gui_scripts': [
            'lindworm.ldmStorageFolderFrm = lindworm.ldmStorageFolderFrm:main',
        ]
    },
)
