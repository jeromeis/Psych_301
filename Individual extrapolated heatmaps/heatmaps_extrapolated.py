import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

CSV_name = input("Participant's code: ")

CSV_path = "./merged_data_participant_" + str(CSV_name) + ".csv"
df = pd.read_csv(CSV_path)

chosen_interval = 50 # precision, to change accordingly
minimum = -175
maximum = 165
ticks_number = 11

x_range = np.linspace(minimum, maximum, chosen_interval+1)  # min, max, np points to get nb intervalticks_number = 10
y_range = np.linspace(maximum, minimum, chosen_interval+1)

to_mean_matrix = np.zeros((chosen_interval, chosen_interval))  # init phase
count_matrix = np.zeros((chosen_interval, chosen_interval))  # init phase

c_points = []
l_points = []

for indexnotused, row in df.iterrows():
    l = row["P2'-P2"]
    c = row["P3'-P3"]
    value = row["decision"]

    l_index = np.subtract(np.digitize(l, y_range), 1)  # because np.digitalize begins at 1 idk why
    c_index = np.subtract(np.digitize(c, x_range), 1)

    to_mean_matrix[l_index, c_index] += value
    count_matrix[l_index, c_index] += 1

    if count_matrix[l_index, c_index] > 0:
        c_points.append(c_index)
        l_points.append(l_index)

meanakaproba_matrix = np.divide(to_mean_matrix, count_matrix, where=count_matrix != 0)
values = [meanakaproba_matrix[l, c] for c, l in zip(c_points, l_points)]
grid_c, grid_l = np.meshgrid(np.arange(chosen_interval), np.arange(chosen_interval))
grid_values = griddata((c_points, l_points), values, (grid_c, grid_l), method='linear', fill_value=np.nan)

fig, ax = plt.subplots(figsize=(10, 10))
heatmap = sns.heatmap(grid_values, cmap="coolwarm", annot=False, fmt='.2f', linewidths=0, cbar_kws={"label": "Decision probability"})

xticks = np.linspace(minimum, maximum, ticks_number)
yticks = np.linspace(maximum, minimum, ticks_number)
plt.xticks(np.linspace(0, chosen_interval, ticks_number), np.round(xticks, 1), rotation=0)
plt.yticks(np.linspace(0, chosen_interval, ticks_number), np.round(yticks, 1), rotation=90)
plt.title(str(CSV_name) + "'s heatmap")
plt.xlabel("Delta breakpoint 3")
plt.ylabel("Delta breakpoint 2")
plt.show()
