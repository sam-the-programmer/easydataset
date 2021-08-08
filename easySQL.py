import pandas as pd
import sqlite3 as sql

from pandas.core.series import Series

class PandaSQL(object):
    
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._dataframe = pd.read_sql(filename)
    
    def insert_column(self, column: int, name: str, value: list or tuple or Series) -> None:
        if column < 0: raise ValueError("Column index must be <= 0.")
        elif name in self._dataframe.columns: raise ValueError("Column name is already in database. Please use a new column name.")
        elif len(value) != len(self._dataframe.iloc(axis=1)[0]): raise ValueError("Value for new column must be of equal length to other columns.")
        
        self._dataframe.insert(column, name, value)
        
    def save(self):
        self._dataframe.to_sql(self._filename)
        
class SQLite(object):
    
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._db = sql.connect(self._filename)
        with self._db as db:
            self._cursor = db.cursor()
            
    def __enter__(self):
        return self
            
    def __exit__(self, type, traceback, value):
        self._cursor.close()
            
    def _commit(self, name):
        self._db.commit()
    
    def create_table(self, name, rules: str):
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}({str(rules)})")
        self._commit(name)
        
    def insert(self, name, values: tuple):
        self._cursor.execute(f"INSERT INTO {name} VALUES{str(values)}")
        self._commit(name)
        
    def clear(self, name):
        self._cursor.execute(f"DELETE FROM {name} WHERE true")
        self._commit(name)
            
    def show(self, name: str):
        self._cursor.execute(f"SELECT * FROM {name}")
        fetched = self._cursor.fetchall()
        for item in fetched:
            print(item)
        self._commit(name)
        return fetched
        
            

with SQLite("birds.db") as database:
    database.clear("names")
    database.create_table("names", "id integer PRIMARY KEY, name text")
    database.insert("names", ("1", "Bob"))
    database.insert("names", ("2", "Jeff"))
    database.insert("names", ("3", "Gerry"))
    database.show("names")