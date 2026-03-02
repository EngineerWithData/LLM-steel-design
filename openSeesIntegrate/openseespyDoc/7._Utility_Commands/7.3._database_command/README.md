# 7.3. database command

# 7.3. database command

database(*type*, *dbName*)
:   Create a database.

    |  |  |
    | --- | --- |
    | `type` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | database type:   * `'File'` - outputs database into a file * `'MySQL'` - creates a SQL database * `'BerkeleyDB'` - creates a BerkeleyDB database |
    | `dbName` ([str](https://docs.python.org/3/library/stdtypes.html#str)) | database name. |