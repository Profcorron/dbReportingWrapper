# dbReportingWrapper
A python module to simplify running a query against a database, where the query is saved as a file.

## Installation
Run:
```
python setup.py build
python setup.py install
```

## Set Up

This module allows you to run a SQL query saved as a .sql file against a database using a connection string defined in a .json file.

SQL Files should be in the format:
```
SELECT *
FROM SOME_TABLE
WHERE VARIABLE = :VARNAME
```

And connection details .json files in the format:
```
{
    "db_driver": "cx_Oracle",
    "db_connection_string": "username/password@server"
}
```

## Usage Examples

Retrieve data
```
import dbreportingwrapper as database

queryFile = os.path.abspath('sql/path/to/file.sql')
dbDetails = os.path.abspath('settings/connectionDetails.json')
paramsDict = {'VARNAME': varValue}
headings, data = database.retrieve_data(dbDetails, queryFile, paramsDict)
```

Insert single row into table
```
rowList = [valA, valB, valC]
commit = insert_data(dbDetails, queryFile, rowList)
```

Insert multiple rows into table
```
rowList = [valA, valB, valC]
dataList = [rowList, rowList]
commit = insert_data_many(dbDetails, queryFile, dataList)
```


