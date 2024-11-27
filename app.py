import streamlit as st
from captions import *
from streamlit_helpers import *
from helpers import get_tables

st.set_page_config(layout="wide")
st.title("Battery Report Analysis")

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

        ## Processing tables
        results = process_tables(recent,battery)
        recent_plot = results['recent_plot']
        summary = results['summary']
        duration_plot = results['duration_plot']
        distribution_plot = results['distribution_plot']



        ## Main Content
        basic_info_section, battery_info_section = st.columns(2) 
        
        ## baisc info Section
        with basic_info_section:
            with st.expander("**Show Basic System Information**",expanded=True):
                write_key_value(basic_info)

        ## battery info section
        with battery_info_section:
            with st.expander("**Show Basic Battery Information**",expanded=True):
                write_key_value(battery_info)

        ## summary section
        summary_section1, summary_section2 = st.columns(2)
        with summary_section1:
            with st.expander("**Summary of Last 36 hours**",expanded=True):
                write_key_value(summary,skip_keys=[
                    "Daily Energy Usage (mWh)",
                    "Daily Active Time (minutes)"
                ])

        with summary_section2:
            with st.expander("**Daily Energy Usage**",expanded=True):
                print(summary["Daily Energy Usage (mWh)"])
                write_key_value(summary["Daily Energy Usage (mWh)"])
            with st.expander("**Daily Active Time**",expanded=True):
                write_key_value(summary["Daily Active Time (minutes)"])

        ## plots section
        st.subheader("Plots")

    
        ## recent plot
        if recent_plot is not None:
            with st.expander("**Recent Usage**",expanded=True):
                st.write(RECENT_USAGE_CAPTION)
                st.image(recent_plot, use_container_width=False)

        ## battery plot
        duration_plot_section, distribution_plot_section = st.columns(2)
        with duration_plot_section:
            if duration_plot is not None:
                with st.expander("**Active Session Durations**",expanded=True):
                    st.write(DURATION_CAPTION)
                    st.image(duration_plot, use_container_width=True)

        with distribution_plot_section:
            if distribution_plot is not None:
                with st.expander("**Active Session Distribution**",expanded=True):
                    st.write(DISTRIBUTION_CAPTION)
                    st.image(distribution_plot,use_container_width=True)



    except Exception as e:
        st.error(f"Error while processing the HTML file: {e}")
else:
    st.info("Please upload an HTML file to proceed.")
