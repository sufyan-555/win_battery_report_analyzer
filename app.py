import streamlit as st
from processing import *
from captions import *
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
        basic_info = tables[0]
        battery_info = tables[1]
        recent = tables[2]
        battery = tables[3]

        ## Main Content
        basic_info_section, battery_info_section = st.columns(2)
        
        ## Processing baisc info
        with basic_info_section:
            with st.expander("**Show Basic System Information**",expanded=True):
                cols = st.columns(2)  # Create two columns for key-value pairs
                for index, row in basic_info.dropna().iterrows():
                    key = row[0]
                    value = row[1]
                    cols[0].write(key)
                    cols[1].write(value)

        ## Processing battery info
        with battery_info_section:
            with st.expander("**Show Basic Battery Information**",expanded=True):
                cols = st.columns(2)  # Create two columns for key-value pairs
                for index, row in battery_info.dropna().iterrows():
                    key = row[0]
                    value = row[1]
                    cols[0].write(key)
                    cols[1].write(value)

        ## Processing recent
        st.subheader("Battery Usage:")
        try:
            plot = process_recent_table(recent)
            st.image(plot, caption=RECENT_USAGE_CAPTION, use_container_width=False)
        except Exception as e:
            st.error(f"Error while processing the table: {e}")

    except Exception as e:
        st.error(f"Error reading the HTML file: {e}")
else:
    st.info("Please upload an HTML file to proceed.")
