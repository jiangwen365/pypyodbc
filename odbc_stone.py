# -*- coding: utf-8 -*-
'''
import pypyodbc
conn=pypyodbc.connect('dsn=mssql')
cur = conn.cursor()
cur.execute('select top 3 product_name from pyodbc_t')
for row in cur.fetchall():
    for field in row:
        print field.decode('mbcs'),
    print ''

import sqlalchemy
engine = sqlalchemy.create_engine('mssql+pypyodbc://mssql')
for row in engine.execute('select top 2 product_name from pyodbc_t'):
    for field in row:
        print field.decode('mbcs'),
    print ''
    '''
#                  Let Python load it's ODBC connecting tool pypyodbc
import os, os.path, time
from pypyodbc1 import win_create_mdb, version
print (version)

for x in range(10):   
    print ('file: '+str(x))
    #import pypyodbc_reuse_param as pypyodbc
    #import pyodbc as pypyodbc
    import pypyodbc2 as pypyodbc
    t_begin = time.time()
    fix = str(x%10)
    if os.path.exists(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb'):
         os.remove(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    if os.path.exists(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb'):
         os.remove(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb')
    win_create_mdb( u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb' )
    
    
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    print (conn.getinfo(pypyodbc.SQL_DRIVER_NAME))
    cur = conn.cursor()
    cur.execute(u"""create table saleout (ID COUNTER PRIMARY KEY, customer_name text,
                            product_name text, 
                            price float, 
                            volume int,
                            sell_time datetime);""")
    
    conn.commit()
    for b in range(2000):
        cur.executemany(u'''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) 
        VALUES(?,?,?,?,?)''',      [(u'杨天真','Apple IPhone 5','5500.1',1,'2012-1-21'),
                                    (u'郑现实','Huawei Ascend D2',None,1,'2012-1-21'),
                                    (u'莫小闵','Huawei Ascend D2','5000.5',2,None),      
                                    (u'顾小白','Huawei Ascend D2','5000.5',1,'2012-1-22')])

        cur.commit()

        if b%100 == 0:
            print b*4,
    
    #cur.execute('INSERT INTO saleout (customer_name,product_name,price,volume,sell_time)  SELECT customer_name,product_name,price,volume,sell_time  FROM saleout;')

    cur.commit()
    
    cur.close()
    
    
    
    conn.commit()
    conn.close()
    print ('\tWrite time: '+str(time.time() - t_begin))
    
    
    
    t_begin = time.time()
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')

    cur = conn.cursor()
    
    win_create_mdb( u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb' )
    conn_copy = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb')


    cur_copy = conn_copy.cursor()
    cur_copy.execute(u"""create table saleout (ID COUNTER PRIMARY KEY, customer_name text,
                            product_name text, 
                            price float, 
                            volume int,
                            sell_time datetime);""")
    cur.execute('select * from saleout')
    r = cur.fetchone()
    r_n = 0
    while r:
        if r_n == 0:
            print r.get('product_name'),r.get('sell_time'),r.get('price')
        cur_copy.execute('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) 
        VALUES(?,?,?,?,?)''',      r[1:])
        cur_copy.commit()
        if r_n % 400 == 0:
            print r_n,
        r = cur.fetchone()
        r_n +=1
    #cur_copy.close()
    conn_copy.close()
    conn.close()
    
    print ('\tR & W time: '+str(time.time() - t_begin))
   
