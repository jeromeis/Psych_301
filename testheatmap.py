import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

CSV_path = "C:/Users/morga/Desktop/pyveea/Cleese/Heatmaps/700floattest.csv"
df = pd.read_csv(CSV_path)

chosen_interval = 10

axis_range = np.linspace(-175, 165, chosen_interval+1)  # min, max, np points to get nb interval

to_mean_matrix = np.zeros((chosen_interval, chosen_interval)) # init phase
count_matrix = np.zeros((chosen_interval, chosen_interval))  # init phase

for indexnotused, row in df.iterrows():
    x = row["p2bis-p2"]
    y = row["p3bis-p3"]
    value = row["Percentgan"]  # to change

    x_index = np.digitize(x, axis_range)-1  # because np.digitalize begins at 1 idk why
    y_index = np.digitize(y, axis_range)-1

    if x_index < chosen_interval and y_index < chosen_interval: #there are some 10 idx idk why 
        to_mean_matrix[x_index, y_index] += value
        count_matrix[x_index, y_index] += 1

meanakaproba_matrix = np.divide(to_mean_matrix, count_matrix, where=count_matrix != 0)

fig, ax = plt.subplots(figsize=(10, 10)) 
heatmap = sns.heatmap(meanakaproba_matrix, cmap="coolwarm", annot=True, fmt='.2f', linewidths=0.5, cbar_kws={'label': 'Proba'})
for i in range(10):
    for j in range(10):
        if count_matrix[i, j] == 0:
            heatmap.add_patch(plt.Rectangle((j+0.03, i+0.03), 0.95, 0.95, fill=True, color='#FFFFFF')) #(j+0.05, i+0.05), 0.925, 0.925, fill=True, color='#262626')

plt.xticks(np.linspace(0, 10, 11), axis_range)
plt.yticks(np.linspace(0, 10, 11), axis_range)
plt.title('Carte de slayeur')
plt.xlabel("Breaktpoint 2")
plt.ylabel("Breaktpoint 3")
plt.show()
