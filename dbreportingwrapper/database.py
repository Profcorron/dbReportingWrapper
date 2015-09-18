#!/usr/bin/env python3
""" Database Wrapper

This python code is to help with common database functions.
In particular it is intended for when queries are stored as individual 
files and connection details stored as json objects.
"""

__author__ = "B Croker and A Guinane"
__copyright__ = "Copyright 2015, B Croker and A Guinane"
__license__ = "MIT"
__version__ = "1.0.0"

import json
import os
import re
import io
import csv
import sys
import logging



def load_query(query_filename):
    """ Reads a query string in from a file
    """
    with open(query_filename) as f:
        return f.read()
        

def get_driver(driver_name):
    """ Load the appropriate driver 
        specified in the settings file
    """
    if driver_name == 'sqlite3':
        import sqlite3 as db_driver
    elif driver_name == 'cx_Oracle':
        import cx_Oracle as db_driver
    elif driver_name == 'pyodbc':
        import pyodbc as db_driver
    elif driver_name == 'pypyodbc':
        import pypyodbc as db_driver
    elif driver_name == 'psycopg2':
        import psycopg2 as db_driver
    elif driver_name == 'PyMySql':
        import PyMySql as db_driver
    elif driver_name == 'pymssql':
        import pymssql as db_driver
    else:
        # TODO: pick a better exception type and message
        raise ImportError
    return db_driver


def connect_to_db(settings_filename):  
    """ Connects to database as object
    """
    # set up a db connection from the settings   
    with open(settings_filename) as f:
        SETTINGS = json.load(f)
    db_driver = get_driver(SETTINGS['db_driver'])
    
    # pymssql uses a different connection string format
    # so have to treat it differently for now
    if SETTINGS['db_driver'] == 'pymssql':
        host = SETTINGS['db_connection_string']['host']
        user = SETTINGS['db_connection_string']['user']
        password = SETTINGS['db_connection_string']['password']
        database = SETTINGS['db_connection_string']['database']
        conn = db_driver.connect(host, user, password, database)
    else:
        conn = db_driver.connect(SETTINGS['db_connection_string'])
        
    return conn


def run_command(settings_filename, query_filename):
    """ Run an insert query for a single row of data
    """
    conn = connect_to_db(settings_filename)
    cursor = conn.cursor()

    query = load_query(query_filename)
    cursor.execute(query)
    conn.commit()
    
    cursor.close()
    conn.close()

    return True

    
def insert_data(settings_filename, query_filename, row_list):
    """ Run an insert query for a single row of data
    """
    conn = connect_to_db(settings_filename)
    cursor = conn.cursor()

    query = load_query(query_filename)
    cursor.execute(query,row_list)
    conn.commit()
    
    cursor.close()
    conn.close()

    return True
    
def insert_data_many(settings_filename, query_filename, data_list):
    """ Run an insert query for multiple rows of data
    """
    conn = connect_to_db(settings_filename)
    cursor = conn.cursor()
    
    query = load_query(query_filename)
    cursor.prepare(query)
    logging.debug(query)
    cursor.executemany(None, data_list)
    conn.commit()
    
    cursor.close()
    conn.close()

    return True   

def retrieve_data(settings_filename, query_filename, params_dict, data_format='list',
                  csv_file_name='',csv_rows_to_write=100000):
    """ Run an select query with a defined set of parameters
    """
    conn = connect_to_db(settings_filename)
    cursor = conn.cursor()

    cursor.execute(load_query(query_filename), params_dict)
    if data_format == 'list':
        # format into a table with header
        query_results = construct_list(cursor)
    elif data_format == 'dict':
        # format into dictionary
        query_results = construct_dict(cursor)
    elif data_format == 'csv':
        # format into csv
        query_results = construct_csv(cursor)
    elif data_format == 'file':
        # format into csv File
        query_results = construct_csv_file(cursor,csv_file_name,csv_rows_to_write)
        
    cursor.close()
    conn.close()


    return query_results

    
def construct_dict(cursor):
    """ transforms the db cursor rows from table format to a
        list of dictionary objects
    """
    rows = cursor.fetchall()
    return [dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in rows]


def construct_list(cursor):
    """ transforms the db cursor into a list of records,
        where the first item is the header
    """
    header = [h[0] for h in cursor.description]
    data = cursor.fetchall()
    return header, data

def construct_csv(cursor):
    """ transforms the db cursor rows into a csv file string
    """
    header, data = construct_list(cursor)
    # python 2 and 3 handle writing files differently
    if sys.version_info[0] <= 2:
        output = io.BytesIO()
    else:
        output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(header)
    for row in data:
        writer.writerow(row)

    return output.getvalue()    

def construct_csv_file(cursor,file_name,row_limit=100000):
    """ transforms the db cursor rows into a csv file string
    """
    if file_name =='':
        logging.error('Csv File cannot be created without a defined filename')


    with open(file_name,'w',newline='') as csv_file:
        writer, output = create_writer()

        header = [h[0] for h in cursor.description]
        writer.writerow(header)
        csv_file.write(output.getvalue())
        #Writer closed to empty it. 
        output.close()

    while True:
        writer, output = create_writer()

        results = cursor.fetchmany(row_limit)
        if not results:
            break
        with open(file_name, 'a', newline='') as csv_file:
            writer.writerows(results)
            csv_file.write(output.getvalue())
            output.close()

    return

def create_writer():
    """ Creates a csv file Writer.
    :return: Returns a Writer and the associated Output
    """
    # python 2 and 3 handle writing files differently
    if sys.version_info[0] <= 2:
        output = io.BytesIO()
    else:
        output = io.StringIO()
    writer = csv.writer(output)
    return writer, output

