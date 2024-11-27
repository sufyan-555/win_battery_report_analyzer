import streamlit as st
import pandas as pd
from processing import *

def write_key_value(df,skip_keys=[]):
    cols = st.columns(2)

    if isinstance(df,pd.DataFrame):
        for index, row in df.dropna().iterrows():
            key = row[0]
            value = row[1]
            cols[0].write(key)
            cols[1].write(value)
    else:
        for key, value in df.items():
            if key not in skip_keys:
                cols[0].write(str(key))
                cols[1].write(value)


def process_tables(recent, battery):
    results = {}

    # recent table
    try:
        results['recent_plot'] = process_recent_table(recent)
    except Exception as e:
        results['recent_plot'] = None
        st.error(f"Error while processing the Recent table: {e}")

    try:
        summary, duration_plot, distribution_plot = process_battery_table(battery)
        results.update({
            'summary': summary,
            'duration_plot': duration_plot,
            'distribution_plot': distribution_plot
        })
    except Exception as e:
        results.update({
            'summary': None,
            'duration_plot': None,
            'distribution_plot': None
        })
        st.error(f"Error while processing the Battery table: {e}")

    return results


