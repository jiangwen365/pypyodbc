# -*- coding: utf-8 -*-
# A script used to check performance of pypyodbc vs similar other modules, like pyodbc
# Let Python load it's ODBC connecting tool pypyodbc

from __future__ import print_function
import os, os.path, time, sys, gc

if len(sys.argv) < 2:
    usage = '''
    usage: [the python interpreter] speed.py [the module to be benchmarked] 
    for example:
    
    python speed.py pypyodbc [connection_string]
    python speed.py pyodbc [connection_string]
    pypy speed.py pypyodbc [connection_string]
    ipy speed.py pypyodbc [connection_string]
    '''
    print (usage)
    exit()
    
localDir = os.path.dirname(os.path.realpath(sys.argv[0]))
if len(sys.argv) >= 3:
    connection_string = sys.argv[2]
    test_mdb = False
else:
    test_mdb = True
    
if test_mdb is True:
    from pypyodbc import win_create_mdb

    temp_folder = localDir+'\\pypyodbc_mdb_test\\'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
else:
    connection_string_copy = connection_string


for x in range(4):   
    print ('file: '+str(x))

    pypyodbc = __import__(sys.argv[1])
    #pypyodbc.pooling = False

    print ('Running with pypyodbc %s' %pypyodbc.version)
    fix = str(x%10)
    
    if test_mdb is True:
        if os.path.exists(temp_folder + u'PerformanceTest'+fix+'.mdb'):
             os.remove(temp_folder + u'PerformanceTest'+fix+'.mdb')
        if os.path.exists(temp_folder + u'PerformanceTest'+fix+'c.mdb'):
             os.remove(temp_folder + u'PerformanceTest'+fix+'c.mdb')
        if os.path.exists(temp_folder + u'PerformanceTest'+fix+'copy.mdb'):
             os.remove(temp_folder + u'PerformanceTest'+fix+'copy.mdb')
        win_create_mdb( temp_folder + u'PerformanceTest'+fix+'.mdb' )
    
    
        conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+temp_folder + u'PerformanceTest'+fix+'.mdb')
    else:
        conn = pypyodbc.connect(connection_string)
        
    print (conn.getinfo(pypyodbc.SQL_DRIVER_NAME))
    cur = conn.cursor()
    
    if test_mdb:
        cur.execute(u"""create table saleout (ID COUNTER PRIMARY KEY, customer_name varchar(255),
                                product_name varchar(255), 
                                price float, 
                                volume int,
                                sell_time datetime);""")
    else:
        cur.execute(u"""IF OBJECT_ID('dbo.saleout', 'U') IS NOT NULL DROP TABLE dbo.saleout;""")
        cur.execute(u"""create table saleout (ID INT IDENTITY(1,1) PRIMARY KEY, customer_name varchar(255),
                                product_name varchar(255), 
                                price float, 
                                volume int,
                                sell_time datetime);""")
    conn.commit()
    
    t_begin = time.time()
    for b in range(5000):
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
    
    #cur.close()
    
    
    
    conn.commit()
    #conn.close()
    write_time = time.time() - t_begin
    print ('\tWrite time: '+str(write_time))
    
    #pypyodbc.win_compact_mdb('D:\\pypyodbc_mdb_test\\PerformanceTest'+fix+'.mdb','D:\\pypyodbc_mdb_test\\PerformanceTest'+fix+'c.mdb')
    
    
    if test_mdb is True:
        conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+temp_folder + u'PerformanceTest'+fix+'.mdb',unicode_results=True)
        #conn = pypyodbc.win_connect_mdb('D:\\pypyodbc_mdb_test\\PerformanceTest'+fix+'.mdb')
        
        win_create_mdb( temp_folder + u'PerformanceTest'+fix+'copy.mdb' )
        conn_copy = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+temp_folder + u'PerformanceTest'+fix+'copy.mdb')

    else:
        conn = pypyodbc.connect(connection_string)
        conn_copy = pypyodbc.connect(connection_string_copy)
    cur = conn.cursor()
    

    cur_copy = conn_copy.cursor()
    if test_mdb:
        cur_copy.execute(u"""create table saleout_copy (ID COUNTER PRIMARY KEY, customer_name varchar(255),
                            product_name varchar(255), 
                            price float, 
                            volume int,
                            sell_time datetime);""")
    else:
        
        cur_copy.execute(u"""IF OBJECT_ID('dbo.saleout_copy', 'U') IS NOT NULL DROP TABLE dbo.saleout_copy;""")
        cur_copy.execute(u"""create table saleout_copy (ID INT IDENTITY PRIMARY KEY, customer_name varchar(255),
                                product_name varchar(255), 
                                price float, 
                                volume int,
                                sell_time datetime);""")
    
    t_begin = time.time()
    cur.execute('select customer_name,product_name,price,volume,sell_time from saleout')
    r = cur.fetchmany(4)
    r_n = 0
    while r:
        #if r_n == 0:
        #    print (r['product_name'],r[:])
        cur_copy.executemany('''INSERT INTO saleout_copy(customer_name,product_name,price,volume,sell_time) 
        VALUES(?,?,?,?,?)''',      r)
        cur_copy.commit()
        if r_n % 400 == 0:
            print (r_n, end='\r')
        r = cur.fetchmany(4)
        r_n +=4
    #cur_copy.close()
    cur_copy.commit()
    #conn_copy.close()
    #conn.close()
    R_W_time = time.time() - t_begin
    print ('\tR & W time: '+str(time.time() - t_begin))
    


    t_begin = time.time()
    
    if test_mdb is True:
        conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+temp_folder + u'PerformanceTest'+fix+'copy.mdb',unicode_results=True)
        #conn = pypyodbc.win_connect_mdb('D:\\pypyodbc_mdb_test\\PerformanceTest'+fix+'.mdb')
    else:
        conn = pypyodbc.connect(connection_string_copy)
    cur = conn.cursor()
    
    cur.execute('select customer_name,product_name,price,volume,sell_time from saleout_copy')
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
    #conn.close()
    
    print ('\tRead  time: '+str(time.time() - t_begin))
    
    
    print ("garbage collected:" + str(gc.collect()), end = ' ')
    print ("garbage count:" + str(gc.garbage.__len__()), end = ' ')
    print ("garbage:" + str(gc.garbage))
   

