import os
import re
import time
# import sqlite3
import pandas as pd
import duckdb

ip = "46.125.249.79"
# ip = '217.182.78.180'

root_path = os.getcwd()
if "Lab5" not in root_path:
    root_path += "\\Lab5\\"
if "src" not in root_path:
    root_path += "src\\"
data_path = root_path + "data\\"
db_path = data_path + "comp.db"
log_path = data_path + "access.log"

nrows = None
# nrows = 100000
t = time.time()
df_raw = pd.read_csv(log_path, sep="\r", header=None, names=["text"],
                     nrows=nrows
                    )
df_raw.reset_index(inplace=True, names="id")
read_time = time.time()-t

connection = duckdb.connect(db_path)
connection.register("raw", df_raw)
# 192.168.0.5 - john [10/Oct/2025:13:55:36 +0200] "GET /index.html HTTP/1.1" 200 1024 "http://example.com" "Mozilla/5.0" ""
t = time.time()
connection.execute(f"""
CREATE OR REPLACE TABLE parsed AS
SELECT
    id,
    regexp_extract(text, '^[0-9.]+', 0) AS ip,
    regexp_extract(text, '\\[(.*?)\\]', 1) AS date,
    regexp_extract(text, '"([^"]*)"', 1) AS url,
    CAST(regexp_extract(text, ' ([0-9]+) ', 1) AS INTEGER) AS status,
    CAST(
        CASE
            WHEN regexp_extract(text, ' ([0-9]+) "', 1) = '' THEN '0'
            ELSE regexp_extract(text, ' ([0-9]+) "', 1)
        END
    AS INTEGER) AS size
FROM raw;
""")

# df_parsed = connection.sql(
#     """
# SELECT * FROM parsed
#     """).df()
# print(df_parsed)
# print(df_parsed[df_parsed["size"]==-1])
# print(df_parsed[df_parsed == ''].nunique())
# print([int(i) for i in df_parsed["size"].unique()])

df_parsed = connection.sql(
    f"""
SELECT status, SUM(size) AS total_size
FROM parsed
WHERE ip = '{ip}'
GROUP BY status
    """).df()
sql_time = (time.time()-t) + read_time
print(df_parsed)

t = time.time()
parsed = []
pattern = re.compile(
                r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?\[(?P<date>.*?)\].*?"(?P<url>.*?)"\s(?P<status>\d+)\s(?P<size>\d+)'
            )
for _, row in df_raw.iterrows():
    match = pattern.search(row["text"])
    if match:
        parsed.append(match.groupdict())
df_parsed = pd.DataFrame(parsed)
df_parsed = df_parsed.astype({
    'size': 'int',
    'status': 'int',
})
df_parsed = df_parsed[df_parsed["ip"] == ip].groupby("status")["size"].sum()

python_time = (time.time()-t) + read_time
print(df_parsed)
print(f"[Time Spent] SQL: {sql_time:.4f} sec | Python {python_time:.4f} sec")
