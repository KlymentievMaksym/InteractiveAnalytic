import os
import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="logs.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)

    def save_dataframe(self, df: pd.DataFrame, table_name: str):
        df.to_sql(table_name, self.connection, if_exists="replace", index=True)

    def load_dataframe(self, table_name):
        return pd.read_sql(f"SELECT * FROM {table_name}", self.connection)

    def query(self, sql: str) -> pd.DataFrame:
        return pd.read_sql_query(sql, self.connection)

    def delete(self):
        # self.connection.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)