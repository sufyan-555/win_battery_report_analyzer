import streamlit as st
import pandas as pd
from processing import *
from helpers import get_tables

st.set_page_config(layout="wide")
st.title("Battery Report Analyzer")

## Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your battery report HTML file", type=["html"])

if uploaded_file:
    ## get tables
    try:
        tables = get_tables(uploaded_file)
        baisc_info = tables[0]
        battery_info = tables[1]
        recent = tables[2]
        battery = tables[3]


        st.success(f"Found {len(tables)} tables in the file.")

        ## Processing baisc info
        ## Processing battery info
        ## Processing recent
        st.subheader("Battery Usage Plot")
        try:
            plot = process_recent_table(recent)
            st.image(plot, caption="Battery Usage Over Time", use_container_width=True)
        except Exception as e:
            st.error(f"Error while processing the table: {e}")

    except Exception as e:
        st.error(f"Error reading the HTML file: {e}")
else:
    st.info("Please upload an HTML file to proceed.")
