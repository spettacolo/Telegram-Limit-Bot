import sqlite3
from typing import List, Tuple, Dict, Any
from contextlib import closing

class Database:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        columns_with_types = ", ".join([f"{col} {typ}" for col, typ in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        self.execute_query(query)
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute_query(query, tuple(data.values()))
    
    def update(self, table_name: str, data: Dict[str, Any], condition: str) -> None:
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.execute_query(query, tuple(data.values()))
    
    def delete(self, table_name: str, condition: str) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute_query(query)
    
    def select(self, table_name: str, columns: List[str], condition: str = "") -> List[Tuple]:
        columns_str = ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.fetch_all(query)

    def select_one(self, table_name: str, columns: List[str], condition: str) -> Tuple:
        columns_str = ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table_name} WHERE {condition}"
        return self.fetch_one(query)

    def count(self, table_name: str, condition: str = "") -> int:
        query = f"SELECT COUNT(*) FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        result = self.fetch_one(query)
        return result[0] if result else 0

    def execute_query(self, query: str, params: Tuple = ()) -> None:
        with closing(self.connection):
            self.cursor.execute(query, params)
            self.connection.commit()

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        with closing(self.connection):
            self.cursor.execute(query, params)
            return self.cursor.fetchall()

    def fetch_one(self, query: str, params: Tuple = ()) -> Tuple:
        with closing(self.connection):
            self.cursor.execute(query, params)
            return self.cursor.fetchone()

    def close(self) -> None:
        self.connection.close()