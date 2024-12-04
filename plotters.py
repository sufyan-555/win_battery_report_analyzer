import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import io
from sklearn.linear_model import LinearRegression

def get_recent_usage_plot(df):
    plt.figure(figsize=(14,6), facecolor='white')
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plot the entire line in blue
    plt.plot(df['START TIME'], df['CAPACITY REMAINING'], 
            color='#1E90FF',  # Dodger blue
            linewidth=2,
            alpha=0.7)

    # Set plot title and axis labels
    start_day = df['START TIME'].min().date()
    end_day = df['START TIME'].max().date()
    plt.title(f'Battery Consumption between {start_day} - {end_day}', 
            fontsize=14, fontweight='bold', color='#333333')
    plt.xlabel('Start Time', fontsize=12, color='#666666')
    plt.ylabel('Capacity Remaining (%)', fontsize=12, color='#666666')

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n %d/%m'))
    plt.xticks(rotation=0, ha='right', fontsize=10, color='#666666')
    plt.yticks(fontsize=10, color='#666666')

    # Set x-axis limits and ticks
    plt.xlim(df['START TIME'].min(), df['START TIME'].max())
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))

    # Add grid
    plt.grid(True, linestyle='--', linewidth=0.5, color='#E0E0E0')

    plt.tight_layout()

    # Save the plot as an image in a BytesIO buffer (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')  # Save to BytesIO in PNG format
    img_buf.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to prevent it from being shown again
    
    return img_buf


def get_active_duration_plot(df):
    plt.figure(figsize=(7,6), facecolor='white')
    plt.title('Active Session Duration in last 36 hours', fontsize=14, fontweight='bold', color='#333333')
    sns.histplot(df['DURATION'][df['DURATION']>0],kde=True,bins=20)
    plt.xlabel('Duration (in minutes)', fontsize=12, color='#666666')
    plt.ylabel('Frequency', fontsize=12, color='#666666')
    plt.xticks(fontsize=10, color='#666666')
    plt.yticks(fontsize=10, color='#666666')
    plt.tight_layout()

    # Save the plot as an image in a BytesIO buffer (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')  # Save to BytesIO in PNG format
    img_buf.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to prevent it from being shown again
    
    return img_buf


def get_active_distribution_plot(df):
    plt.figure(figsize=(7,6), facecolor='white')
    plt.title('Distribution of Active Session Start Times', fontsize=14, fontweight='bold', color='#333333')
    sns.histplot(df['START TIME'].dt.hour,kde=True,bins=24)
    plt.xlabel('Hour of the day', fontsize=12, color='#666666')
    plt.ylabel('Frequency', fontsize=12, color='#666666')
    plt.xticks(fontsize=10, color='#666666')
    plt.yticks(fontsize=10, color='#666666')
    plt.tight_layout()
    plt.show()

    # Save the plot as an image in a BytesIO buffer (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')  # Save to BytesIO in PNG format
    img_buf.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to prevent it from being shown again
    
    return img_buf


def get_battery_capacity_plot(df):
    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Line plot
    plt.plot(df['START DATE'], df['CAPACITY'], color='#1E90FF',  # Dodger blue
            label="Capacity (%)", linewidth=2, alpha=0.8)

    # Title and labels
    plt.title("Battery Full Charge Capacity Over Time", fontsize=18, fontweight="bold", color="#333333")
    plt.xlabel("Start Date", fontsize=12, color="#666666")
    plt.ylabel("Capacity (%)", fontsize=12, color="#666666")

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(ha='left', fontsize=10, color="#666666")
    plt.yticks(fontsize=10, color="#666666")

    # Set y-axis range
    plt.ylim(0, 100)

    # Add grid and legend
    plt.grid(True, linestyle='--', linewidth=0.5, color='#E0E0E0', alpha=0.7)
    plt.legend(fontsize=10, loc="best")

    # Save the plot as an image in a BytesIO buffer (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')  # Save to BytesIO in PNG format
    img_buf.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to prevent it from being shown again
    
    return img_buf


def get_battery_backup_loss_plot(df):
    # Drop rows where 'START DATE' or 'LOSS' contains NaN
    df = df.dropna(subset=['START DATE', 'LOSS'])

    # Convert 'LOSS' to minutes for easier visualization
    df['LOSS (minutes)'] = df['LOSS'].dt.total_seconds() / 60

    # Convert dates to numeric values (this is needed for sklearn's LinearRegression)
    x = mdates.date2num(df['START DATE'])  # Convert dates to numeric format
    x = x.reshape(-1, 1)  # Reshape x for sklearn (2D array)

    y = df['LOSS (minutes)']

    # Create the Linear Regression model
    model = LinearRegression()
    model.fit(x, y)

    # Get the trend line values
    trend_line = model.predict(x)

    # Create the plot
    plt.figure(figsize=(10, 5), facecolor="white")
    plt.style.use('seaborn-v0_8-whitegrid')

    # Line plot for LOSS
    plt.plot(df['START DATE'], df['LOSS (minutes)'], label="Loss (minutes)", linewidth=2, color="lightblue")

    # Plot the trend line
    plt.plot(df['START DATE'], trend_line, label="Trend Line", color="green", linestyle="--", linewidth=2)

    # Title and labels
    plt.title("Battery Life Lost Over Time", fontsize=16, fontweight="bold", color="#333333")
    plt.xlabel("Start Date", fontsize=14, color="#666666")
    plt.ylabel("Battery Backup Lost (min)", fontsize=14, color="#666666")

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(ha='right', fontsize=12, color="#666666")
    plt.yticks(fontsize=12, color="#666666")

    # Add grid and legend
    plt.grid(True, linestyle='--', linewidth=0.5, color='#E0E0E0', alpha=0.7)
    plt.legend(fontsize=10, loc="best")

    # Ensure the trend line is visible
    plt.tight_layout()

    # Save the plot as an image in a BytesIO buffer (in-memory)
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')  # Save to BytesIO in PNG format
    img_buf.seek(0)  # Rewind the buffer to the beginning
    plt.close()  # Close the plot to prevent it from being shown again
    
    return img_buf