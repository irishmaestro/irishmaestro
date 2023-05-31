from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

json_data = sys.argv[1]
data = json.loads(json_data)
df = pd.DataFrame(data['profile']['graphData'])
sns.set(style="dark")
plt.style.use('dark_background')

current_month = datetime.now().replace(day=1)
month_labels = []
for i in range(12):
    month_labels.append(current_month.strftime('%b%y').upper())
    current_month -= timedelta(days=current_month.day)
month_labels.reverse()

fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# line_plot
colors = sns.color_palette('rocket', len(df.columns))
linestyles = ['-', '--', ':']
sns.despine(top=True, right=True)
for col, color, linestyle in zip(df.columns[:3], colors, linestyles):
    axs[0].plot(df[col], label=col, color=color, linestyle=linestyle)
axs[0].legend()
axs[0].set_xticks(range(12))
axs[0].set_xticklabels(month_labels, rotation=45)
axs[0].spines['bottom'].set_color('#17273b')  
axs[0].spines['left'].set_color('#17273b')

# heatmap
cmap = sns.color_palette("rocket", as_cmap=True)
heatmap = sns.heatmap(df.T, annot=True, cmap=cmap, square=True, linewidths=0.5, linecolor="#17273b", ax=axs[1])
heatmap.set_facecolor('black')
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0)
heatmap.set_xticklabels(month_labels, rotation=0)

plt.tight_layout()
plt.savefig('htb_achievement_graph.png', dpi=300)
