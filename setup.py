try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pypyodbc

setup(
    name='pypyodbc',
<<<<<<< HEAD
    version='1.3.1',
=======
    version=pypyodbc.version,
>>>>>>> forked/master
    description='A Pure Python ctypes ODBC module',
    author='jiangwen365',
    author_email='jiangwen365@gmail.com',
    url='https://github.com/jiangwen365/pypyodbc',
    py_modules=['pypyodbc'],
    long_description="""
      A Pure Python ctypes ODBC module compatible with PyPy and almost totally same usage as pyodbc
      """,
<<<<<<< HEAD
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
      ],
      keywords='Python, Database, Interface, ODBC, PyPy',
      license='MIT',
      install_requires=[
        'setuptools',
        'python-dateutil',
      ],
      )
=======
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
    keywords='Python, Database, Interface, ODBC, PyPy',
    license='MIT',
)
>>>>>>> forked/master
