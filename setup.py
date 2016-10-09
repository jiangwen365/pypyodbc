import sys
if len(sys.argv) == 1:
    sys.argv.append('install')

try:
    from setuptools import setup
except:
    from distutils.core import setup


setup(
    name='pypyodbc',
    version='1.3.1',
    description='A Pure Python ctypes ODBC module',
    author='jiangwen365',
    author_email='jiangwen365@gmail.com',
    url='http://code.google.com/p/pypyodbc/',
    py_modules=['pypyodbc'],
      long_description="""\
      A Pure Python ctypes ODBC module compatible with PyPy and almost totally same usage as pyodbc
      """,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Development Status :: 4 - Beta",
      ],
      keywords='Python, Database, Interface, ODBC, PyPy',
      license='MIT',
      install_requires=[
        'setuptools',
      ],
      )
