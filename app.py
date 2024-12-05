import streamlit as st
from captions import *
from streamlit_helpers import *
from model import *
from helpers import get_tables
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")
st.title("Battery Report Analysis")

## Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your battery report HTML file", type=["html"])

    # Instructions for the user
    st.markdown(
        """
        ### How to Generate Your Battery Report
        1. Open Command Prompt (Windows).
        2. Type the following command and press Enter:
           ```
           powercfg/batteryreport output "C:\\battery-report.html"
           ```
        3. Locate the generated `battery-report.html` file in the specified directory.
        4. Upload the file here to analyze your battery's performance.
        
        If still facing issues, you can [watch this video for step-by-step instructions](https://www.youtube.com/watch?v=zevIiiWBs1c) to generate your battery report.
        
        """
    )

if uploaded_file:
    ## get tables
    try:
        tables = get_tables(uploaded_file)
        basic_info = tables[0]
        battery_info = tables[1]
        recent = tables[2]
        battery = tables[3]
        capacity = tables[5]
        life = tables[6]
        battery_backup = tables[7]

        ## Processing tables
        results = process_tables(recent,battery,capacity,life,battery_backup)
        recent_plot = results['recent_plot']
        duration_plot = results['duration_plot']
        distribution_plot = results['distribution_plot']
        capacity_plot = results['capacity_plot']
        life_plot = results['life_plot']


        ## Processing Data for AI Summary
        data = str(basic_info)+ str(battery_info) + str(results['summary'])
        plots = [recent_plot, duration_plot, distribution_plot, capacity_plot, life_plot] 

        ## Main Content

        ## Ai Summary
        try:
            st.header("AI Summary")
            with st.spinner("Generating AI Summary..."):
                ai_summary = summarize_with_ai(summary,plots)
                st.markdown(ai_summary)
        except Exception as e:
            st.error(f"Sorry Could not generate AI Summary: {e}")

        ## General content
        st.header("Detailed Report")
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
                write_key_value(results['summary'])

        with summary_section2:
            with st.expander("**Daily Energy Usage**",expanded=True):
                write_key_value(results["daily_energy_usage"])
            with st.expander("**Daily Active Time**",expanded=True):
                write_key_value(results["daily_active_time"])


        ## plots section
        st.subheader("Plots")

        ## battery capacity and loss plot
        with st.expander(f"**Loss in Battery Capacity**",expanded=True):
            capacity_info_section, capacity_plot_section = st.columns([2,3])
            with capacity_info_section:
                st.write(CAPACITY_LOSS_CAPTION)
            with capacity_plot_section:
                st.image(capacity_plot, use_container_width=True)

        with st.expander(f"**Loss in Backup**",expanded=True):
            life_plot_section, life_info_section = st.columns([3,2])
            with life_plot_section:
                st.image(life_plot,use_container_width=True)
            with life_info_section:
                st.write(LIFE_LOSS_CAPTION)

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
