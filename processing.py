from helpers import *
from plotters import *

def process_recent_table(recent):
    handle_time(recent,'START TIME')
    remove_percent(recent,'CAPACITY REMAINING')
    plot = get_usage_plot(recent)
    return plot