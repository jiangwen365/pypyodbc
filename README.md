pypyodbc
========

A pure Python Cross Platform ODBC interface module


**This is the GitHub homepage of pypyodbc**  

Also check out the  [Wiki](https://github.com/jiangwen365/pypyodbc/wiki) and [Version History](https://github.com/jiangwen365/pypyodbc/wiki/Version-History)


Features
--------

  * One pure Python script, runs on CPython / IronPython / PyPy , Python 3.3 / 2.4 / 2.5 / 2.6 / 2.7 , Win / Linux , 32 / 64 bit
  * Almost totally same usage as pyodbc (can be seen as a re-implementation of pyodbc in pure Python via ctypes)
  * Simple - the whole module is implemented in a single python script with less than 3000 lines
  * [Built-in Access MDB file creation and compression functions](https://github.com/jiangwen365/pypyodbc/wiki/Access-MDB-support) on Windows 

Simply try pypyodbc:

```python
# Microsoft Access DB
import pypyodbc 

connection = pypyodbc.win_create_mdb('D:\\database.mdb')

SQL = 'CREATE TABLE saleout (id COUNTER PRIMARY KEY,product_name VARCHAR(25));'
connection.cursor().execute(SQL)
...


#SQL Server 2000/2005/2008 (and probably 2012 and 2014)
import pypyodbc as pyodbc # you could alias it to existing pyodbc code (not every code is compatible)
db_host = 'serverhost'
db_name = 'database'
db_user = 'username'
db_password = 'password'
connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';UID=' + db_user + ';PWD=' + db_password + ';'
db = pyodbc.connect(connection_string)
SQL = 'CREATE TABLE saleout (id COUNTER PRIMARY KEY,product_name VARCHAR(25));'
connection.cursor().execute(SQL)

# Doing a simple SELECT query
connStr = (
    r'Driver={SQL Server};'
    r'Server=sqlserver;'
    #r'Server=127.0.0.1,52865;' +
    #r'Server=(local)\SQLEXPRESS;'
    r'Database=adventureworks;'
    #r'Trusted_Connection=Yes;'
    r'UID=sa;'
    r'PWD=sapassword;'
    )
db = pypyodbc.connect(connStr)
cursor = db.cursor()

# Sample with just a raw query:
cursor.execute("select client_name, client_lastname, [phone number] from Clients where client_id like '01-01-00%'")

# Using parameters (IMPORTANT: YOU SHOULD USE TUPLE TO PASS PARAMETERS)
# Python note: a tuple with just one element must have a trailing comma, otherwise is just a enclosed variable
cursor.execute("select client_name, client_lastname, [phone number] "
"from Clients where client_id like ?", ('01-01-00%', ))

# Sample, passing more than one parameter
cursor.execute("select client_name, client_lastname, [phone number] "
"from Clients where client_id like ? and client_age < ?", ('01-01-00%', 28))

# Method 1, simple reading using cursor
while True:
    row = cursor.fetchone()
    if not row:
        break
    print "Client Full Name (phone number): ", row['client_name'] + ' ' +  row['client_lastname'] + '(' + row['phone number'] + ')'

# Method 2, we obtain dict's all records are loaded at the same time in memory (easy and verbose, but just use it with a few records or your app will consume a lot of memory), was tested in a modern computer with about 1000 - 3000 records just fine...
import pprint; pp = pprint.PrettyPrinter(indent=4)
columns = [column[0] for column in cursor.description]
for row in cursor.fetchall():
    pp.pprint(dict(zip(columns, row)))

# Method 3, we obtain a list of dict's (represents the entire query)
query_results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
pp.pprint(query_results)

# When cursor was used must be closed, if you will not use again the db connection must be closed too.
cursor.close()
db.close()
```

Install
-------

If you have pip available:

    pip install pypyodbc

Or get the latest pypyodbc.py script from GitHub (Main Development site) <https://github.com/jiangwen365/pypyodbc>

Double click the setup.py file, or run

    python setup.py install

