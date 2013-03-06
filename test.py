# -*- coding: utf-8 -*-
import sys, os, time
from decimal import Decimal


def main():
    for database_name, conn_string, create_table_sql in database_strings:
        source_to_test = [
        'Access',
        'SQLServer',
        #'MySQL',
        'PostgreSQL'
        ]
        if database_name in source_to_test:
            print_header(database_name)
        else:
            database_name+' skipped.'
            continue
        
        print 'Connecting database server with pypyodbc...'
        conn = pypyodbc.connect(conn_string, ansi = False,  unicode_results = True, readonly = False, timeout = 2)

        print conn.getinfo(pypyodbc.SQL_SERVER_NAME)
        print conn.getinfo(pypyodbc.SQL_DATABASE_NAME)
        print conn.getinfo(pypyodbc.SQL_PROCEDURES)
        print conn.getinfo(pypyodbc.SQL_MAX_DRIVER_CONNECTIONS)
        
        print 'Has table "pypyodbc_test_tabl"?   ',
        cur = conn.cursor()
        has_table_data = cur.tables(table='pypyodbc_test_tabl').fetchone()
        cur.close()
        
        
        if has_table_data:
            print 'pypyodbc_test_tabl exists. Dropping the existing pypyodbc_test_tabl now.',
            cur = conn.cursor()
            cur.execute ('Drop table pypyodbc_test_tabl')
        else:
            print 'pypyodbc_test_tabl does not exist',
            cur = conn.cursor()
            
        if hasattr(cur,'execdirect'):
            cur.execdirect(create_table_sql)
        else:
            cur.execute(create_table_sql)
        cur.commit()
        
        print ('pypyodbc_test_tabl has been created. Now listing the columns:')
        for row in cur.columns(table='pypyodbc_test_tabl').fetchall():
            print row
        cur.close()
        
        print 'Inserting rows now with execute()...  ',
        start_time = time.time()
        cur = conn.cursor()
        cur.execute(u"insert into pypyodbc_test_tabl values(1,'Hello! 这是pypyodbc模块',12.3,1234.55,'2012-11-11','17:31:32','2012-11-11',NULL, ?)", (binary_logo,))

        longtext = u''.join([u'我在马路边，捡到一分钱。']*25)
        cur.execute("insert into pypyodbc_test_tabl values (?,?,?,?,NULL,NULL,NULL,NULL,?)", \
                                (2, \
                                longtext,\
                                Decimal('1233.4513'), \
                                123.44, \
#                                datetime.datetime.now(), \
#                                datetime.datetime.now().time(),\
#                                datetime.date.today(),\
                                mv))
        row_num = 1500
        print 'Inserting 5*'+str(row_num)+' rows now with executemany()...  ',
        for i in xrange(3,row_num):
            cur.executemany(u"""insert into pypyodbc_test_tabl values 
            (?,?,12.32311, 1234.55, NULL,NULL,'2012-12-23',NULL,NULL)""", 
            [
            (i+500000, "【巴黎圣母院】".decode('utf-8')),
            (i+100000, u"《普罗米修斯》"),
            (i+200000, longtext),
            (i+300000, '〖!@#$$%"^&%&〗'.decode('utf-8')),
            (i+400000, "querty-','"),
            ]\
            )
        
        end_time = time.time()
        
        print 'Inserting completed, total time ',
        print end_time-start_time,
        conn.commit()
        print ' Commit comlete, commit time ',
        print time.time() - end_time 

        print 'Excute selecting from pypyodbc_test_tabl... '
        if database_name in ['Access','MySQL']:
            # Access and MySQL do not support batch SQL, so can not test the nextset() method.
            cur.execute(u"""select * from pypyodbc_test_tabl""")
            print cur.description
            
            
            #Get results
            field = cur.fetchone()[-1]#.bin_logo
            file(cur_file_dir()+'\\logo_'+database_name+'.gif','wb').write(field)
            field = cur.fetchone()[-1]#.bin_logo
            file(cur_file_dir()+'\\logo2_'+database_name+'.gif','wb').write(field)
            
            
            
            for row in cur.fetchmany(6):
                for field in row:
                    print type(field),
                    if isinstance(field, unicode): print field.encode('mbcs'),
                    elif isinstance(field, bytearray): pass
                    else: print field,
                print ('')
            
            
            
            cur.close()
            #conn.rollback()
            cur = conn.cursor()
            start_time =  time.time()
            print 'Updating one column...',
            cur.execute(u'update pypyodbc_test_tabl set 数量 = ? where 数量 > 0 '.encode('mbcs'),(time.time(),))
            print 'Updated: '+str(cur.rowcount)+' rows',
            print ' Total time: '+ str(time.time()-start_time)
            
        else:
            cur.execute(u"""select * from pypyodbc_test_tabl;update pypyodbc_test_tabl set kong = 5 where ID = 2;select ID, kong, riqi, product_name from pypyodbc_test_tabl where ID = 2 """)
            print cur.description

            
            #Get results
            field = cur.fetchone()[-1]#.bin_logo
            file(cur_file_dir()+'\\logo_'+database_name+'.gif','wb').write(field)
            field = cur.fetchone()[-1]#.bin_logo
            file(cur_file_dir()+'\\logo2_'+database_name+'.gif','wb').write(field)


            
            for row in cur.fetchmany(6):
                for field in row:
                    print type(field),
                    if isinstance(field, unicode): print field.encode('mbcs'),
                    elif isinstance(field, bytearray): pass
                    else: print field,
                print ('')
            

            cur.nextset()
            print 'After calling nextset, get the information of updated: '+str(cur.rowcount)+' rows'
            cur.nextset()
            
            for field in cur.fetchone():
                if isinstance(field, unicode):
                    print field.encode('mbcs')+'\t',
                elif isinstance(field, bytearray):
                        pass
                else:
                    print str(field)+'\t',
            print ('')


            print ' Total time: '+ str(time.time()-start_time)
        cur.close()
        conn.commit()
        cur = conn.cursor()
        for field in cur.execute(u"""select * from pypyodbc_test_tabl""").fetchone():
            if isinstance(field, unicode):
                print field.encode('mbcs')+'\t',
            elif isinstance(field, bytearray):
                    pass
            else:
                print str(field)+'\t',
        print ('')
        
        start_time = time.time()
        i = 1
        row = cur.fetchone()
        cur.skip(1500)
        while row != None:
            for field in row:
                x = field
            i += 1
            if i % 1000 == 0:
                print i,
            
            row = cur.fetchone()
        print '    Total records retrive time:',
        print time.time() - start_time
        #print conn.FetchAll()
        #Close before exit
        cur.close()

        #cProfile.run('prof_func()')

        #conn.close()
    print ('End of testing')
    time.sleep(3)
    

        
        



def cur_file_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


import base64
binary_data = base64.b64decode('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')

if os.path.exists(cur_file_dir()+'/Logo.gif'):
    binary_data = file(cur_file_dir()+'/Logo.gif','rb').read()
binary_logo = bytearray(binary_data)
mv = bytearray(binary_data)


#c_Path = ctypes.create_string_buffer(u"CREATE_DB=.\\e.mdb General\0\0".encode('mbcs'))
#ODBC_ADD_SYS_DSN = 1
#ctypes.windll.ODBCCP32.SQLConfigDataSource(None,ODBC_ADD_SYS_DSN,"Microsoft Access Driver (*.mdb)", c_Path)


def u8_enc(v, force_str = False):
    if v == None: return ('')
    elif isinstance(v,unicode): return (v.encode('utf_8','replace'))
    elif isinstance(v, buffer): return ('')
    else:
        if force_str: return (str(v))
        else: return (v)



def print_header(database_name):
    print ' *'.join(['' for i in range(40)])
    print ' '*30 + database_name 
    print ' *'.join(['' for i in range(40)])

        

if __name__ == "__main__":
    if 'pyodbc' in sys.argv:
        print 'Running with pyodbc'
        import pyodbc as pypyodbc
    else:
        print 'Running with pypyodbc'
        import pypyodbc
        
        
    print pypyodbc.version    
    mdb_path = cur_file_dir()+'\\e.mdb'
    
    if hasattr(pypyodbc,'win_create_mdb') and sys.platform in ('win32','cli'):
        pypyodbc.win_create_mdb('"'+mdb_path+'"')
            
    database_strings = [\
        ('Access',
        u'''Driver={Microsoft Access Driver (*.mdb)};DBQ='''+mdb_path,
        u"""create table pypyodbc_test_tabl (ID integer PRIMARY KEY,product_name text,数量 numeric,价格 float,日期 
                datetime,shijian time,riqi datetime, kong float, bin_logo LONGBINARY)""",
        ),
        ('SQLServer',
        'DSN=MSSQL',
        u"""create table pypyodbc_test_tabl (ID integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                datetime,shijian varchar(20),riqi varchar(20), kong float, bin_logo varbinary(8000))""",
        ),
        ('MySQL',
        'DSN=MYSQL',
        u"""create table pypyodbc_test_tabl (ID integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                datetime,shijian time,riqi date, kong float, bin_logo BLOB)""",
        
        ),
        ('PostgreSQL',
        'DSN=PostgreSQL35W',
        u"""create table pypyodbc_test_tabl (ID integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                        timestamp,shijian time,riqi date, kong float, bin_logo bytea)""",
        ),
        ]
        
        
    pypyodbc.DEBUG = 0
    DSN_list = pypyodbc.dataSources()
    print (DSN_list)
        
        
    if 'profile' in sys.argv:
        import cProfile
        cProfile.run('main()')
    else:
        main()
    if hasattr(pypyodbc,'win_compact_mdb') and sys.platform in ('win32','cli'):
        mdb_file_path = '"'+mdb_path.encode('mbcs')+'"'
        pypyodbc.win_compact_mdb(mdb_file_path,mdb_file_path.replace('.mdb','_compact.mdb'))
