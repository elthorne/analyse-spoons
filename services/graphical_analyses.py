import matplotlib.pyplot as plt
import json
import os
from datetime import datetime
from collections import Counter
import seaborn as sns
import pandas as pd
from collections import defaultdict


def plot_activity_over_time(data_dir):
    # ick
    dates = []
    totals = []

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for date, items in data.items():
                    total = next((item['Total'] for item in items if 'Total' in item), 0)
                    dates.append(datetime.strptime(date, "%Y-%m-%d"))
                    totals.append(total)

    # TODO: This is probably why it's ick
    plt.plot(dates, totals, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Total Tasks')
    plt.title('Activity Over Time')
    plt.grid(True)
    plt.show()


def plot_top_activities(data_dir, top_x):
    activity_counter = Counter()

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for items in data.values():
                    for item in items:
                        if 'name' in item:
                            activity_name = item['name'].split(' (')[0]  # Remove numbers in parentheses
                            activity_counter[activity_name] += 1

    most_common = activity_counter.most_common(top_x)
    activities, counts = zip(*most_common)

    plt.barh(activities, counts)
    plt.xlabel('Count')
    plt.title(f'Top {top_x} Activities')
    plt.gca().invert_yaxis()
    plt.show()


def plot_monthly_activity_heatmap(data_dir):
    month_activity = {}

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for date, items in data.items():
                    year, month, _ = date.split('-')
                    key = f"{year}-{month}"
                    total = next((item['Total'] for item in items if 'Total' in item), 0)
                    month_activity[key] = month_activity.get(key, 0) + total

    # Prepare encrypted_data for heatmap
    heatmap_data = pd.Series(month_activity).unstack().fillna(0)

    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu")
    plt.title('Monthly Activity Summary')
    plt.show()


def plot_activity_distribution(data_dir):
    activity_counter = Counter()

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for items in data.values():
                    for item in items:
                        if 'name' in item:
                            activity_name = item['name'].split(' (')[0]
                            activity_counter[activity_name] += 1

    activities, counts = zip(*activity_counter.items())

    plt.pie(counts, labels=activities, autopct='%1.1f%%')
    plt.title('Activity Distribution')
    plt.show()


def plot_cumulative_activity(data_dir):
    dates = []
    cumulative_totals = []
    cumulative_sum = 0

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for date, items in data.items():
                    total = next((item['Total'] for item in items if 'Total' in item), 0)
                    cumulative_sum += total
                    dates.append(datetime.strptime(date, "%Y-%m-%d"))
                    cumulative_totals.append(cumulative_sum)

    plt.plot(dates, cumulative_totals, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Tasks')
    plt.title('Cumulative Activity Over Time')
    plt.grid(True)
    plt.show()


def plot_monthly_totals_comparison(data_dir):
    monthly_totals = defaultdict(int)

    for file in os.listdir(data_dir):
        if file.endswith(".json"):
            with open(os.path.join(data_dir, file), 'r') as f:
                data = json.load(f)
                for date, items in data.items():
                    year, month, _ = date.split('-')
                    key = f"{year}-{month}"
                    total = next((item['Total'] for item in items if 'Total' in item), 0)
                    monthly_totals[key] += total

    months, totals = zip(*sorted(monthly_totals.items()))

    plt.bar(months, totals)
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Total Tasks')
    plt.title('Monthly Totals Comparison')
    plt.show()




