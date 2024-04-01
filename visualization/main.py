import streamlit as st
import pandas as pd

upload_file = st.file_uploader("报考院校", type=['xlsx'])
if upload_file is None:
    st.stop()


@st.cache_data
def load_data():
    """缓存函数"""
    st.write("Loading data...")
    return pd.read_excel(upload_file, sheet_name=None)


dfs = load_data()

names = list(dfs.keys())

sheet_selects = st.multiselect('工作表', names, [])

if len(sheet_selects) == 0:
    st.stop()

tabs = st.tabs(sheet_selects)

for tab, name in zip(tabs, sheet_selects):
    with tab:
        df = dfs[name]
        st.dataframe(df)
