from datetime import datetime
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import sys

json_data = sys.argv[1]
htb_rank_data = json.loads(json_data)
lowest_rank = htb_rank_data["data"]["rank"]
lowest_rank_date = htb_rank_data["data"]["date"]
data = htb_rank_data["data"]["rank_chart_data"]

current_date = datetime.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

dates = pd.date_range(end=pd.Timestamp(year=current_year, month=current_month, day=current_day), periods=12, freq='M')
dates = pd.date_range(end=pd.Timestamp(year=2023, month=6, day=1), periods=12, freq='M')
df = pd.DataFrame({'Date': dates, 'Rank': pd.Series(data)})
df['Rank'].replace(0, np.nan, inplace=True)

sns.set(style="dark")
sns.set_palette("dark")

plt.style.use('dark_background')

ax = sns.lineplot(x='Date', y='Rank', data=df.dropna(), color='#0f1a27', marker='D', markersize=6, markeredgecolor='lime')

gradient = np.linspace(0, 1, len(df['Rank'].dropna()) + 2)
colors = sns.color_palette("cubehelix", len(df['Rank'].dropna()) + 2)[1:]
ax.fill_between(df['Date'], 0, df['Rank'].fillna(df['Rank'].min()), color=colors, alpha=0.3)

for _, row in df.dropna().iterrows():
    ax.text(row['Date'], row['Rank'] + 20, int(row['Rank']), color='lime', ha='center', va='bottom', fontsize=5)

plt.title("htb_rank", color='lime')
plt.xlabel("")
plt.ylabel("")
date_format = mdates.DateFormatter('%b%y')
ax.xaxis.set_major_formatter(date_format)
plt.xticks(rotation=45, color='lime')
plt.yticks(range(0, 700, 100), color='lime')

ax.grid(False)
sns.despine(top=True, right=True)
ax.spines['bottom'].set_color('#0f1a27')
ax.spines['left'].set_color('#0f1a27')

lowest_rank_text = f"Best Rank: {int(lowest_rank)} @ {lowest_rank_date}"
ax.text(df['Date'].iloc[-1], 50, lowest_rank_text, color='lime', ha='right', va='bottom', fontsize=8)

plt.savefig("htb_rank_graph.png", dpi=300, bbox_inches='tight', transparent=True)
