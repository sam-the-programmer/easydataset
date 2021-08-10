import csv
import sqlite3 as sql
import warnings

import pandas as pd
from pandas.core.series import Series


class PandaTable(object):
    
    def __init__(self, table: str, filename: str, always_save = False) -> None:
        """
        PandaSQL is an object class for reading
        and writing to SQL with Pandas. It is presently
        not implemented fully. Please use an SQLite
        object or easySQL object."""
        warnings.warn(UserWarning("This is a very new beta class. Please report any issues to the github repository."))
        self._filename = filename
        self._alwaysSave = always_save
        self._dataframe = pd.read_sql(table, filename)
    
    def get_item(self, column: str or int, row: str or int) -> str:
        if type(column) == str:
            column = self._dataframe.columns.index(column)
        if type(row) == str:
            row = self._dataframe.columns.index(row)
            
        return str(self._dataframe.iloc()[column].iloc()[row])
    
    def set_item(self, column: str or int, row: str or int):
        if type(column) == str:
            column = self._dataframe.columns.index(column)
        if type(row) == str:
            row = self._dataframe.columns.index(row)
            
        if self._alwaysSave: self.save()
        return 
    
    def insert_column(self, column: int, name: str, value: list or tuple or Series) -> None:
        if column < 0: raise ValueError("Column index must be <= 0.")
        elif name in self._dataframe.columns: raise ValueError("Column name is already in database. Please use a new column name.")
        elif len(value) != len(self._dataframe.iloc(axis=1)[0]): raise ValueError("Value for new column must be of equal length to other columns.")
        
        self._dataframe.insert(column, name, value)
        if self._alwaysSave: self.save()
        
    def save(self) -> None:
        self._dataframe.to_sql(self._filename)
        
class SQLite(object):
    
    def __init__(self, filename: str) -> None:
        """
        This is an object class that allows you
        to write and read the files. The database
        is auto-commited to, so you don't need to
        worry about commiting."""
        self._filename = filename
        self._db = sql.connect(self._filename)
        with self._db as db:
            self._cursor = db.cursor()
            
    def __enter__(self):
        return self
            
    def __exit__(self, type, traceback, value):
        self._cursor.close()
            
    def commit(self):
        """Commit to the database."""
        self._db.commit()
    
    def create_table(self, name, rules: str):
        """Create a new table, with all rules, including indexing primary key."""
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}({str(rules)})")
        self.commit()
        
    def insert(self, name, values: tuple):
        """Insert a value at the specified location."""
        self._cursor.execute(f"INSERT INTO {name} VALUES{str(values)}")
        self.commit()
        
    def clear(self, name):
        """Clear the table and commit that."""
        try:
            self._cursor.execute(f"DELETE FROM {name} WHERE TRUE")
            self.commit()
        except sql.OperationalError:
            print(f"{name} table not cleared, since it doesn't exist.")
            
    def show(self, name: str):
        """Print the entire table."""
        self._cursor.execute(f"SELECT * FROM {name}")
        fetched = self._cursor.fetchall()
        for item in fetched:
            print(str(list(item)).replace("[", "").replace("]", ""))
        self.commit()
        return fetched
        
class easySQL(object):
    def __init__(self, filename: str) -> None:
        """This object is a simpler version of
        the SQLite object. Much easier to use."""
        self._filename = filename
        self._db = sql.connect(self._filename)
        with self._db as db:
            self._cursor = db.cursor()
            
    def __enter__(self):
        return self
            
    def __exit__(self, type, traceback, value):
        self._cursor.close()
            
    def commit(self):
        """Commit to the database."""
        self._db.commit()
    
    def create_table(self, name, rules: str):
        """Create a table with indexing automatically done for you."""
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}(id integer PRIMARY KEY{str(rules)})")
        self.commit()
        
    def insert(self, name, index, values: tuple):
        """Insert the values to the specified location, with indexing already done for you."""
        self._cursor.execute(f"INSERT INTO {name} VALUES({index},{str(*values)})")
        self.commit()
        
    def clear(self, name):
        """Clear the table selected"""
        try:
            self._cursor.execute(f"DELETE FROM {name} WHERE TRUE")
            self.commit()
        except sql.OperationalError:
            print(f"{name} table not cleared, since it doesn't exist.")
            
    def show(self, name: str):
        """Print the entire table."""
        self._cursor.execute(f"SELECT * FROM {name}")
        fetched = self._cursor.fetchall()
        for item in fetched:
            print(str(list(item)).replace("[", "").replace("]", ""))
        self.commit()
        return fetched
            
class easyCSV(object):
    def __init__(self, filename: str) -> None:
        """A simplified version of the csv module's csv.reader()."""
        self._filename = filename
        with open(filename) as file:
            self._raw = csv.reader(file.readlines())
    
    def get_item(self, column: int, row: int) -> any:
        return self._raw[column][row]
    
    def set_item(self, column: int, row: int, value: any) -> None:
        self._raw[column][row] = value
            
    def save(self):
        with open(self._filename, 'w') as file:
            file.write(csv.writer(self._raw))

if __name__ == "__main__":
    with SQLite("names.db") as database:
        database.clear("names")
        database.create_table("names", "id integer PRIMARY KEY, name text")
        database.insert("names", ("1", "Bob"))
        database.insert("names", ("2", "Jeff"))
        database.insert("names", ("3", "Gerry"))
        database.show("names")