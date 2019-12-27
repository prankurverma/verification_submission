from distutils.core import setup, Extension

name = "sha256"      # name of the module
version = "1.0"  # the module's version number

setup(name=name, version=version,
      # distutils detects .i files and compiles them automatically
      ext_modules=[Extension(name='_sha256', # SWIG requires _ as a prefix for the module name
                             sources=["sha256.i", "src/sha256.c"],
                             include_dirs=['src'])
    ])
