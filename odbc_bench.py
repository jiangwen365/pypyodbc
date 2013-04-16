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

from __future__ import print_function
import os, os.path, time, sys
from pypyodbc import win_create_mdb


for x in range(120):   
    print ('file: '+str(x))
    #import pypyodbc_reuse_param as pypyodbc
    #import pyodbc as pypyodbc
    if 'pyodbc' in sys.argv:
        import pyodbc as pypyodbc
        print ('Running with pyodbc %s' %pypyodbc.version)
    else:
        import pypyodbc as pypyodbc
        print ('Running with pypyodbc %s' %pypyodbc.version)
    t_begin = time.time()
    fix = str(x%10)
    if os.path.exists(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb'):
         os.remove(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    if os.path.exists(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'c.mdb'):
         os.remove(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'c.mdb')
    if os.path.exists(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb'):
         os.remove(u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb')
    win_create_mdb( u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb' )
    
    
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    print (conn.getinfo(pypyodbc.SQL_DRIVER_NAME))
    cur = conn.cursor()
    cur.execute(u"""create table saleout (ID COUNTER PRIMARY KEY, customer_name varchar(255),
                            product_name varchar(255), 
                            price float, 
                            volume int,
                            sell_time datetime);""")
    
    conn.commit()
    for b in range(2500):
        cur.executemany(u'''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) 
        VALUES(?,?,?,?,?)''',      [(u'杨天真','Apple IPhone 5','5500.1',1,'2012-1-21'),
                                    (u'郑现实','Huawei Ascend D2',None,1,'2012-1-21'),
                                    (u'莫小闵','Huawei Ascend D2','5000.5',2,'2012-1-21'),      
                                    (u'顾小白','Huawei Ascend D2','5000.5',None,'2012-1-22')])

        
        cur.commit()
        if b%100 == 0:
            print (b*4, end='\r')
            
    
    #cur.execute('INSERT INTO saleout (customer_name,product_name,price,volume,sell_time)  SELECT customer_name,product_name,price,volume,sell_time  FROM saleout;')

    cur.commit()
    
    cur.close()
    
    
    
    conn.commit()
    conn.close()
    write_time = time.time() - t_begin
    print ('\tWrite time: '+str(write_time))
    
    #pypyodbc.win_compact_mdb('D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb','D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'c.mdb')
    
    t_begin = time.time()
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb',unicode_results=True)
    #conn = pypyodbc.win_connect_mdb('D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    cur = conn.cursor()
    
    win_create_mdb( u'D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb' )
    conn_copy = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb')


    cur_copy = conn_copy.cursor()
    cur_copy.execute(u"""create table saleout (ID COUNTER PRIMARY KEY, customer_name varchar(255),
                            product_name varchar(255), 
                            price float, 
                            volume int,
                            sell_time datetime);""")
    cur.execute('select customer_name,product_name,price,volume,sell_time from saleout')
    r = cur.fetchmany(4)
    r_n = 0
    while r:
        #if r_n == 0:
        #    print (r['product_name'],r[:])
        cur_copy.executemany('''INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) 
        VALUES(?,?,?,?,?)''',      r)
        cur_copy.commit()
        if r_n % 400 == 0:
            print (r_n, end='\r')
        r = cur.fetchmany(4)
        r_n +=4
    #cur_copy.close()
    cur_copy.commit()
    conn_copy.close()
    conn.close()
    R_W_time = time.time() - t_begin
    print ('\tR & W time: '+str(time.time() - t_begin))
    


    t_begin = time.time()
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'copy.mdb',unicode_results=True)
    #conn = pypyodbc.win_connect_mdb('D:\\pypyodbc_mdb_test\\YourMDBfilepath'+fix+'.mdb')
    cur = conn.cursor()
    
    cur.execute('select customer_name,product_name,price,volume,sell_time from saleout')
    r = cur.fetchmany(4)
    r_n = 0
    while r:
        #if r_n == 0:
        #    print (r['product_name'],r[:])

        if r_n % 400 == 0:
            print (r_n, end='\r')
        r = cur.fetchmany(4)
        r_n +=4
    #cur_copy.close()
    conn.close()
    
    print ('\tRead  time: '+str(time.time() - t_begin))
   
