#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
import pyodbc
import pandas as pd
import os

def converter():
    '''
    Function to transform MS Access database to
    a foldes containing .csv files
    '''

    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_name = [file for file in os.listdir(dir_path) if file.endswith('.accdb')][0]
    os.rename(r'{dir_path}/{db_name}'.format(
                    dir_path=dir_path,
                    db_name=db_name),
            r'{dir_path}/db.accdb'.format(
                dir_path=dir_path
            ))
    db_name = 'db.accdb'
    output_folder = '{dir_path}/NPRI_files/'.format(dir_path=dir_path)
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    path = r'{dir_path}/{db_name}'.format(dir_path=dir_path,
                                          db_name=db_name)
    driver = r'Microsoft Access Driver (*.mdb, *.accdb)'

    connection_string = '''
    Driver={driver};
    DBQ={dbq};
    Trusted_Connetion=yes;
    '''.format(
            driver=driver,
            dbq=path
            )

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    table_names = [x.table_name for x in cursor.tables(tableType='TABLE')]
    for tb_name in table_names:
        cursor = conn.cursor()
        c_names = [row.column_name for row in cursor.columns(table=tb_name)]
        df_dict = {}
        for c_name in c_names:
            sql = r'select {col} from {name}'.format(col=c_name,
                                                     name=tb_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            df_dict.update({c_name: [row[0] for row in cursor.fetchall()]})
        df = pd.DataFrame(df_dict)
        df.to_csv('{output_folder}{tb_name}.csv'.format(
                                                    output_folder=output_folder,
                                                    tb_name=tb_name
                                                        ),
                  sep=',',
                  index=False,
                  encoding='utf-8')

    conn.close()

    if os.path.exists(path):
        os.remove(path)
