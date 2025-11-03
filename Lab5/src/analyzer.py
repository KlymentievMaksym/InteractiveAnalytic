import pandas as pd
import time

class LogAnalyzer:
    def __init__(self, db):
        self.db = db

    def analyze_by_ip(self, ip: str, limit: int = 3) -> pd.DataFrame:
        query = f"""
        SELECT status, SUM(size) AS total_size
        FROM parsed_logs
        WHERE ip = '{ip}'
        GROUP BY status
        """
        # ORDER BY total_size DESC
        # LIMIT {limit}
        return self.db.query(query)

    def compare_performance(self, df_parsed: pd.DataFrame, ip: str):
        t1 = time.time()
        db_stats = self.analyze_by_ip(ip)
        sql_time = time.time() - t1

        t2 = time.time()
        py_stats = df_parsed[df_parsed["ip"] == ip].groupby("status")["size"].sum()
        py_stats.columns = ["status", "total_size"]
        py_time = time.time() - t2

        return sql_time, py_time, db_stats, py_stats
