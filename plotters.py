import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import io

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