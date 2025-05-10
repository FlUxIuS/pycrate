# -*- coding: UTF-8 -*-

import os
import sys

# Directly import distutils to avoid setuptools dependency
# This is a workaround for Python 3.12 where distutils is not in the standard library
if not hasattr(sys, 'distutils_path'):
    sys.distutils_path = True
    try:
        import setuptools
    except ImportError:
        # Create a minimal version of what we need from setuptools
        import distutils.core as setuptools
        setuptools.find_packages = lambda: [
            "pycrate_core",
            "pycrate_ether",
            "pycrate_media",
            "pycrate_asn1c",
            "pycrate_asn1dir",
            "pycrate_asn1rt",
            "pycrate_csn1",
            "pycrate_csn1dir",
            "pycrate_mobile",
            "pycrate_diameter",
            "pycrate_corenet",
            "pycrate_sys",
            "pycrate_crypto",
            "pycrate_osmo",
            "pycrate_gmr1",
            "pycrate_gmr1_csn1",
        ]

# Pycrate Version
VERSION = "0.7.9"

# get long description from the README.md
try:
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as fd:
        long_description = fd.read()
except (IOError, UnicodeDecodeError):
    long_description = "Pycrate - Protocol and format handling library"

# Determine which setup function to use
if 'setuptools' in sys.modules:
    from setuptools import setup, find_packages
else:
    from distutils.core import setup
    def find_packages():
        return [
            "pycrate_core",
            "pycrate_ether",
            "pycrate_media",
            "pycrate_asn1c",
            "pycrate_asn1dir",
            "pycrate_asn1rt",
            "pycrate_csn1",
            "pycrate_csn1dir",
            "pycrate_mobile",
            "pycrate_diameter",
            "pycrate_corenet",
            "pycrate_sys",
            "pycrate_crypto",
            "pycrate_osmo",
            "pycrate_gmr1",
            "pycrate_gmr1_csn1",
        ]

# Use a more compatible setup call
kwargs = {
    "name": "pycrate",
    "version": VERSION,
    "packages": find_packages(),
    "license": "LGPL v2.1+",
    "author": "Benoit Michau",
    "author_email": "michau.benoit@gmail.com",
    "description": "A software suite to handle various data and protocol formats",
    "url": "https://github.com/pycrate-org/pycrate/",
    "keywords": "protocol format ASN.1 CSN.1 compiler encoder decoder mobile core network Diameter NAS S1AP NGAP TCAP MAP GTP PFCP SCCP ISUP",
}

# Add optional arguments if setuptools is available
if 'setuptools' in sys.modules:
    kwargs.update({
        "test_suite": "test.test_pycrate",
        "scripts": [
            "tools/pycrate_asn1compile.py",
            "tools/pycrate_berdecode.py",
            'tools/pycrate_certdecode.py',
            "tools/pycrate_showmedia.py",
            "tools/pycrate_shownas.py",
            "tools/pycrate_gtp_type_info.py",
            "tools/pycrate_map_op_info.py",
            "tools/pycrate_extnas_demo.py",
        ],
        "install_requires": [],
        "extras_require": {
            "NASLTE": ["CryptoMobile"],
            "NAS5G": ["CryptoMobile"],
            "corenet": ["pysctp", "CryptoMobile"],
            "diameter_dict": ["lxml"],
            "SEDebugMux": ["crcmod"],
        },
        "package_data": {
            "pycrate_corenet": ["AuC.db"],
        },
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
    })

# Execute setup
setup(**kwargs)
