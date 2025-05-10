# -*- coding: UTF-8 -*-

import os
import sys

# Handle the distutils import for Python 3.12
try:
    import distutils.ccompiler as dist_ccomp
    import distutils.command.build as dist_build
    from setuptools import setup, Extension
    from setuptools.command.install import install
    SETUPTOOLS_AVAILABLE = True
except ImportError:
    # Fallback for Python 3.12 where distutils is removed
    import subprocess
    import platform
    SETUPTOOLS_AVAILABLE = False
    
    # Define a minimal Extension class
    class Extension:
        def __init__(self, name, sources):
            self.name = name
            self.sources = sources

def rename_files(dirpath, fromsuf, tosuf):
    for fn in os.listdir(dirpath):
        if fn.endswith(fromsuf):
            os.rename(dirpath + fn, dirpath + fn[:-len(fromsuf)] + tosuf)

# Determine compiler type
is_msvc = False
if SETUPTOOLS_AVAILABLE:
    is_msvc = dist_ccomp.get_default_compiler() == 'msvc'
else:
    # Try to determine compiler without distutils
    is_msvc = platform.system() == 'Windows' and 'msvc' in subprocess.check_output('cc -v', shell=True, text=True, stderr=subprocess.STDOUT).lower()

# Define extensions
if is_msvc:
    # MSVC requires C files to be actually C++ in order to compile them with
    # support for "modern" C features
    print('compiling C extensions with MSVC: renaming .c to .cc')
    rename_files('./C_alg/', '.c', '.cc')
    rename_files('./C_py/', '.c', '.cc')
    pycomp128 = Extension('pycomp128', sources=['C_py/pycomp128.cc', 'C_alg/comp128.cc'])
    pykasumi  = Extension('pykasumi',  sources=['C_py/pykasumi.cc', 'C_alg/Kasumi.cc'])
    pysnow    = Extension('pysnow',    sources=['C_py/pysnow.cc', 'C_alg/SNOW_3G.cc'])
    pyzuc     = Extension('pyzuc',     sources=['C_py/pyzuc.cc', 'C_alg/ZUC.cc'])
    pykeccakp1600 = Extension('pykeccakp1600', sources=['C_py/pykeccakp1600.cc', 'C_alg/KeccakP-1600-3gpp.cc'])
else:
    pycomp128 = Extension('pycomp128', sources=['C_py/pycomp128.c', 'C_alg/comp128.c'])
    pykasumi  = Extension('pykasumi',  sources=['C_py/pykasumi.c', 'C_alg/Kasumi.c'])
    pysnow    = Extension('pysnow',    sources=['C_py/pysnow.c', 'C_alg/SNOW_3G.c'])
    pyzuc     = Extension('pyzuc',     sources=['C_py/pyzuc.c', 'C_alg/ZUC.c'])
    pykeccakp1600 = Extension('pykeccakp1600', sources=['C_py/pykeccakp1600.c', 'C_alg/KeccakP-1600-3gpp.c'])

def postop():
    if is_msvc:
        # reverting the renaming
        rename_files('./C_alg/', '.cc', '.c')
        rename_files('./C_py/', '.cc', '.c')

# Use setuptools if available or invoke gcc directly
if SETUPTOOLS_AVAILABLE:
    class build_wrapper(dist_build.build):
        def run(self):
            # on windows: rename *.c to *.cc
            # on linux: should run OK
            dist_build.build.run(self)
            postop()

    class install_wrapper(install):
        def run(self):
            # on windows: rename *.c to *.cc
            # on linux: should run OK
            install.run(self)
            postop()
            
    # Read README for long description
    try:
        with open('README.md', 'r') as f:
            long_description = f.read()
    except:
        long_description = "CryptoMobile provides Python bindings to reference implementations in C of mobile cryptographic algorithms"
            
    setup(
        name='CryptoMobile',
        version='0.3',
        cmdclass={'install': install_wrapper, 'build': build_wrapper},
        packages=['CryptoMobile'],
        ext_modules=[pycomp128, pykasumi, pysnow, pyzuc, pykeccakp1600],
        test_suite="test.test_CryptoMobile",
        author='Benoit Michau',
        author_email='michau.benoit@gmail.com',
        description='CryptoMobile provides (C)Python bindings to reference implementations '\
                    'in C of mobile cryptographic algorithms: Comp128, Milenage, TUAK, Kasumi, SNOW-3G, ZUC',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/mitshell/CryptoMobile/',
        keywords='cryptography mobile network Kasumi SNOW ZUC Milenage Comp128 TUAK',
        license='GPLv2+',
    )
else:
    # Fallback for Python 3.12 without setuptools - manually compile and install
    print("Setuptools not available. Using manual compilation...")
    
    # Create build directories
    os.makedirs('build', exist_ok=True)
    os.makedirs('build/lib', exist_ok=True)
    
    # Compile each extension
    for ext in [pycomp128, pykasumi, pysnow, pyzuc, pykeccakp1600]:
        ext_name = ext.name + ('.pyd' if is_msvc else '.so')
        sources = ' '.join(ext.sources)
        cmd = f"cc -fPIC -shared -o build/lib/{ext_name} {sources}"
        print(f"Compiling {ext_name}: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    
    # Copy Python package
    import shutil
    if not os.path.exists('build/lib/CryptoMobile'):
        os.makedirs('build/lib/CryptoMobile', exist_ok=True)
    
    # Copy Python files
    for file in os.listdir('CryptoMobile'):
        if file.endswith('.py'):
            shutil.copy2(f'CryptoMobile/{file}', f'build/lib/CryptoMobile/{file}')
    
    # Create __init__.py
    with open('build/lib/CryptoMobile/__init__.py', 'w') as f:
        f.write('# CryptoMobile package\n')
        f.write('__version__ = "0.3"\n')
    
    print("Manual build completed. Files are in build/lib/")
    print("To install, copy these files to your site-packages directory.")
    
    # Cleanup
    postop()
