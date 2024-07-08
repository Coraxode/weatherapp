import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use as matplotlib_use
from io import BytesIO
import base64


def get_visualizations(weather_data: dict, num_of_records: int) -> tuple:
    def plot_and_encode(df, x, y, label, ylabel, title, color=None):
        plt.figure(figsize=(9, 4.5))
        plt.plot(df[x], df[y], label=label, color=color)
        plt.ylabel(ylabel)
        plt.xlabel("Date")
        plt.title(title)
        plt.tight_layout()
        if num_of_records > 15:
            plt.xticks(rotation=45, fontsize=8)
        if num_of_records > 50:
            plt.xticks(rotation=90, fontsize=6)
        if num_of_records > 90:
            plt.xticks([])

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img

    matplotlib_use('SVG')
    df = pd.DataFrame(weather_data)
    descriptive_stats = df.describe().round(2)
    descriptive_stats = descriptive_stats.drop(index="count")
    descriptive_stats.columns = ["Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "UV Index"]
    descriptive_stats.index = ["Avg value", "Standard Deviation", "Min value", "25th Percentile", "50th Percentile", "75th Percentile", "Max value"]
    descriptive_stats = descriptive_stats.to_html(classes="table", border=0)

    visualizations = {}
    visualizations['img_avg_temperature'] = plot_and_encode(df, 'date', 'avg_temperature', 'Avg Temperature', 'Temperature (°C)', 'Average Temperature', color='red')
    visualizations['img_avg_humidity'] = plot_and_encode(df, 'date', 'avg_humidity', 'Average Humidity', 'Humidity (%)', 'Average Humidity')
    visualizations['img_avg_wind_speed'] = plot_and_encode(df, 'date', 'avg_wind_speed', 'Average Wind Speed', 'Speed (m/s)', 'Average Wind Speed', color='grey')
    visualizations['img_max_uv_index'] = plot_and_encode(df, 'date', 'max_uv_index', 'Max UV Index', 'UV Index', 'Max UV Index', color='purple')

    return visualizations, descriptive_stats
