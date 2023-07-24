import sys
from os import environ
import pandas as pd

import mysql.connector
import streamlit as st
from dotenv import load_dotenv

from utils.utils import load_lottieurl
from streamlit_lottie import st_lottie

load_dotenv()

try:
    db = mysql.connector.connect(
        host=environ.get("HOST"),
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASSWORD"),
        database=environ.get("DB"),
    )

    db_cursor = db.cursor()

except mysql.connector.Error as e:
    print(e)
    print("Error Code:", e.errno)
    print("SQLSTATE", e.sqlstate)
    print("Message", e.msg)
    st.error(e)

st.set_page_config(layout="wide")

lottie_coding = load_lottieurl(
   "https://assets8.lottiefiles.com/datafiles/WSLNdGMeDvnhQMZ/data.json"
)

st_lottie(lottie_coding, height=200, key="Update logo")
st.write("---")

st.markdown(
      """<h1 style='text-align: center;background-color: lightblue'>Read Table</h1>""",
      
    unsafe_allow_html=True,
)
st.write("---")

st.subheader("Select the table to view the contents")


def show_all(table: str):
    q = "select * from %s" % (table)
    db_cursor.execute(q)
    return db_cursor.fetchall()


table = st.selectbox(
    "table_type",
    (
        "customer",
        "bill",
        "food_item",
        "offers",
        "orders",
        "relatives",
        "reservation",
        "resort",
        "room_service",
    ),
    label_visibility="hidden",
    key="customer",
)

try:
    r = show_all(table)

    _, col_m, _ = st.columns([2.5, 10, 1])

    with col_m:
        st.markdown(f"#### Total Entries - `{len(r)}`")
        df = pd.DataFrame(r, columns=[i[0] for i in db_cursor.description])
        df.index = [i + 1 for i in df.index]
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(e)

db.close()
print("DB connection closed")
