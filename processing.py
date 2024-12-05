from helpers import *
from plotters import *


def process_recent_table(recent):
    handle_time(recent,'START TIME')
    remove_percent(recent,'CAPACITY REMAINING')
    plot = get_recent_usage_plot(recent)
    return plot

def process_battery_table(df):
    #) Preprocessing with helper functions
    df = df.dropna(axis=0, how='any')
    df['ENERGY DRAINED'] = df['ENERGY DRAINED'].replace('-',np.nan)
    df['ENERGY DRAINED.1'] = df['ENERGY DRAINED.1'].replace('-',np.nan)
    handle_time(df, 'START TIME')  # Parse and split 'START TIME' into datetime
    handle_duration(df, 'DURATION')  # Convert 'DURATION' to minutes
    remove_percent(df, 'ENERGY DRAINED')  # Clean and convert 'ENERGY DRAINED' column
    remove_mwh(df, 'ENERGY DRAINED.1')  # Clean and convert 'ENERGY DRAINED.1' column

    # Total energy drained
    total_energy_drained = df['ENERGY DRAINED.1'].sum()

    # Total time in active and standby states
    total_active_time = df.loc[df['STATE'] == 'Active', 'DURATION'].sum()
    total_standby_time = df.loc[df['STATE'] == 'Connected standby', 'DURATION'].sum()

    # Average energy drained per state
    avg_energy_drained_active = df.loc[df['STATE'] == 'Active', 'ENERGY DRAINED.1'].mean()
    avg_energy_drained_standby = df.loc[df['STATE'] == 'Connected standby', 'ENERGY DRAINED.1'].mean()
    
    # Longest and shortest active periods
    longest_active_period = df.loc[df['STATE'] == 'Active', 'DURATION'].max()
    shortest_active_period = df.loc[df['STATE'] == 'Active', 'DURATION'].min()

    # Daily usage patterns
    df['Date'] = df['START TIME'].dt.date  # Extract the date
    daily_energy_usage = df.groupby('Date')['ENERGY DRAINED.1'].sum().reset_index()  # Total energy per day
    daily_active_time = df[df['STATE'] == 'Active'].groupby('Date')['DURATION'].sum().reset_index()  # Active time per day

    # Results summary
    results = {
        "Total Energy Drained (mWh)": str(total_energy_drained.round(2)),
        "Total Active Time (minutes)": str(total_active_time.round(2)),
        "Total Standby Time (minutes)": str(total_standby_time.round(2)),
        "Average Energy Drained in Active State (mWh)": str(avg_energy_drained_active.round(2)),
        "Average Energy Drained in Standby (mWh)": str(avg_energy_drained_standby.round(2)),
        "Longest Active Period (minutes)": str(longest_active_period.round(2)),
        "Shortest Active Period (minutes)": str(shortest_active_period.round(2))
    }

    ## Generating the plots
    duration_plot = get_active_duration_plot(df)
    distribution_plot = get_active_distribution_plot(df)

    return [results,daily_energy_usage,daily_active_time], duration_plot, distribution_plot

def process_capacity_table(df):
    df['START DATE'] = df['PERIOD'].apply(get_start_date_form_range)
    remove_mwh(df,'FULL CHARGE CAPACITY')
    remove_mwh(df,'DESIGN CAPACITY')
    df['CAPACITY'] = (df['FULL CHARGE CAPACITY'].astype(int)/df['DESIGN CAPACITY'].astype(int))*100
    df['START DATE'] = pd.to_datetime(df['START DATE'], errors='coerce')

    plot = get_battery_capacity_plot(df)

    return plot

def process_life_table(df):
    df.columns = df.columns.droplevel(0)
    df = df.drop(['CONNECTED STANDBY','Unnamed: 3_level_1','CONNECTED STANDBY'],axis=1)
    df.columns = ['PERIOD','ACTIVE TRUE','ACTIVE DESIGN']
    df['ACTIVE TRUE'] = pd.to_timedelta(df['ACTIVE TRUE'],errors='coerce')
    df['ACTIVE DESIGN'] = pd.to_timedelta(df['ACTIVE DESIGN'],errors='coerce')
    df['LOSS']  = df['ACTIVE DESIGN'] - df['ACTIVE TRUE']
    df['START DATE'] = df['PERIOD'].apply(get_start_date_form_range)
    df['START DATE'] = pd.to_datetime(df['START DATE'], errors='coerce')

    plot = get_battery_backup_loss_plot(df)

    return plot
