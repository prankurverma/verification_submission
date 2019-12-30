from distutils.core import setup, Extension

name = "sha256"      # name of the module
version = "1.0"  # the module's version number

setup(name=name,
      version=version,
      ext_modules=[
                   Extension(
                              name='_sha256',
                              sources=["sha256.i", "src/sha256.c"],
                              include_dirs=['src']
                            )
                   ],
      py_modules = ["sha256"]
     )
