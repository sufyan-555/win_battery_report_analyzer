import streamlit as st
import pandas as pd
from processing import *

def write_key_value(df):
    if isinstance(df,dict):
        df = pd.DataFrame(list(df.items()), columns=["Key", "Value"])

    df = df.dropna()
    df.columns = ["Key", "Value"]
    st.dataframe(df,use_container_width=True,hide_index=True)


def process_tables(recent, battery,capacity,life,battery_backup):
    results = {}

    # recent table
    try:
        results['recent_plot'] = process_recent_table(recent)
    except Exception as e:
        results['recent_plot'] = None
        st.error(f"Error while processing the Recent table: {e}")

    # battery table
    try:
        
        textual_summary, duration_plot, distribution_plot = process_battery_table(battery)
        summary = textual_summary[0]
        daily_energy_usage = textual_summary[1]
        daily_active_time = textual_summary[2]
        ## adding to the battery backup section here
        summary['Expected Battery Backup Now'] = battery_backup.values[0][1]
        summary['Expected Battery Backup when new'] = battery_backup.values[0][4]
        results.update({
            'summary': summary,
            'duration_plot': duration_plot,
            'distribution_plot': distribution_plot,
            'daily_energy_usage': daily_energy_usage,
            'daily_active_time': daily_active_time
        })
    except Exception as e:
        results.update({
            'summary': None,
            'duration_plot': None,
            'distribution_plot': None
        })
        st.error(f"Error while processing the Battery table: {e}")

    # battery capacity table
    try:
        battery_capacity_plot = process_capacity_table(capacity)
        results['capacity_plot'] = battery_capacity_plot
    except Exception as e:
        results['capacity_plot'] =None
        st.error(f"Eror while processing Battery capacity plot: {e}")

    # life table
    try:
        life_plot = process_life_table(life)
        results['life_plot'] = life_plot
    except Exception as e:
        results['life_plot'] = None
        st.error(f"Error while processing Battery life plot : {e}")
        
    return results


