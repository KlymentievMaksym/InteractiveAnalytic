import os
import streamlit as st
import pandas as pd
import time
from database import DatabaseManager
from parser import LogParser
from analyzer import LogAnalyzer
from visualizer import Visualizer
from ip_info import IPInfo


# path_to_log = st.file_uploader("Завантаж файл логів", type=["log", "txt"])
path_to_root = "Lab5/src/"
path_to_data = path_to_root + "data/"
path_to_log = path_to_data + "access.log"
path_to_db = path_to_data + "logs.db"

db = DatabaseManager(path_to_db)
analyzer = LogAnalyzer(db)
parser = LogParser()
visualizer = Visualizer(st)
ipinfo_client = IPInfo()

st.set_page_config(page_title="Лог-Аналізатор", page_icon="📊", layout="wide")
st.title("📊 Аналіз логів сервера")


def read_and_parse_create(path_to_log):
    with st.spinner("Reading log...", show_time=True):
        df_raw = pd.read_csv(path_to_log, sep="\r", header=None, names=["text"])
    with st.spinner("Parsing log...", show_time=True):
        df_parsed = parser.parse_logs(df_raw)
        with st.spinner("Saving parsed readings...", show_time=True):
            db.save_dataframe(df_parsed, "parsed_logs")
    st.session_state.df_parsed = df_parsed
    return df_parsed

def read_and_parse_load():
    with st.spinner("Reading saved log...", show_time=True):
        if "df_parsed" not in st.session_state:
            df_parsed = db.load_dataframe("parsed_logs")
            st.session_state.df_parsed = df_parsed
        else: df_parsed = st.session_state.df_parsed
    return df_parsed

if st.button("Recreate data"):
    if "df_parsed" in st.session_state: del st.session_state.df_parsed
    db.delete()

t1 = time.time()
if os.path.exists(path_to_db) and os.path.getsize(path_to_db) > 0: df_parsed = read_and_parse_load()
else: df_parsed = read_and_parse_create(path_to_log)
print(f"[ ] Done for: {(time.time()-t1):.4f} sec")
df_parsed = df_parsed.astype({
    'size': 'int',
    'status': 'int',
})


# ip_list = df_parsed["ip"].unique()
# selected_ip = st.selectbox("Оберіть IP для аналізу", ip_list)
selected_ip = st.text_input("Напишіть IP для аналізу", '46.125.249.79')

# stats = analyzer.analyze_by_ip(selected_ip)
# st.dataframe(stats)

sql_t, py_t, db_stats, py_stats = analyzer.compare_performance(df_parsed, selected_ip)
st.write(f"SQL: {sql_t:.4f} сек | Python: {py_t:.4f} сек")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Using Database")
    st.dataframe(db_stats)
with col2:
    st.markdown("### Using Python")
    st.dataframe(py_stats)

stats = py_stats / py_stats.sum()
fig = visualizer.show_chart(stats.reset_index())
visualizer.save_chart(fig)

ip_data = ipinfo_client.get_info(selected_ip)
st.subheader(f"🌍 Інформація про IP: {selected_ip}")
st.json(ip_data)
