pypyodbc
========

A pure Python Cross Platform ODBC interface module


** The homepage of pypyodbc is at http://code.google.com/p/pypyodbc/, while here is the coding and development space for pypyodbc.**

Features
--------

  * One pure Python script, runs on CPython / IronPython / PyPy , Python 3.3 / 2.4 / 2.5 / 2.6 / 2.7 , Win / Linux , 32 / 64 bit
  * Almost totally same usage as pyodbc (can be seen as a re-implementation of pyodbc in pure Python via ctypes)
  * Simple - the whole module is implemented in a single python script with less than 3000 lines
  * Built-in Access MDB file creation and compression functions on Windows 

Simply try pypyodbc:

    import pypyodbc 
    pypyodbc.win_create_mdb('D:\\database.mdb')
    connection_string = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\database.mdb'
    connection = pypyodbc.connect(connection_string)
    SQL = 'CREATE TABLE saleout (id COUNTER PRIMARY KEY,product_name VARCHAR(25));'
    connection.cursor().execute(SQL)
    ...

BBS
---

http://tech.groups.yahoo.com/group/pypyodbc/messages


Install
-------

If you have pip available:

    pip install pypyodbc

Or get the latest pypyodbc.py script from GitHub (Main Development site) <https://github.com/jiangwen365/pypyodbc>

Double click the setup.py file, or run

    setup.py install

Also check out the Google wiki at http://code.google.com/p/pypyodbc/
