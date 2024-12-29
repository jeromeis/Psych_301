import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import csv
import os

CSV_name = input("Participant's code: ")

CSV_path = "./merged_data_participant_"+str(CSV_name)+".csv"
df = pd.read_csv(CSV_path)

chosen_interval = 10
minimum=-175
maximum=165

x_range = np.linspace(minimum, maximum, chosen_interval+1)  # min, max, np points to get nb interval
y_range = np.linspace(maximum, minimum, chosen_interval+1)

to_mean_matrix = np.zeros((chosen_interval, chosen_interval)) # init phase
count_matrix = np.zeros((chosen_interval, chosen_interval))  # init phase

for indexnotused, row in df.iterrows():
    l = row["P2'-P2"]
    c = row["P3'-P3"]
    value = row["decision"]

    l_index = np.subtract(np.digitize(l, y_range),1) # because np.digitalize begins at 1 idk why
    c_index = np.subtract(np.digitize(c, x_range),1)

    to_mean_matrix[l_index, c_index] += value
    count_matrix[l_index, c_index] += 1

meanakaproba_matrix = np.divide(to_mean_matrix, count_matrix, where=count_matrix != 0)

fig, ax = plt.subplots(figsize=(10, 10)) 
heatmap = sns.heatmap(meanakaproba_matrix, cmap="coolwarm", annot=True, fmt='.2f', linewidths=0.5, cbar_kws={"label": "Decision probability"})
for i in range(10):
    for j in range(10):
        if count_matrix[i, j] == 0:
            heatmap.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color='#FFFFFF')) #(j+0.05, i+0.05), 0.925, 0.925, fill=True, color='#262626')

#spearman_seg2, p_value_seg2 = spearmanr(axis_range[1:chosen_interval+1], np.mean(meanakaproba_matrix,axis=0))
#spearman_seg3, p_value_seg3 = spearmanr(axis_range[1:chosen_interval+1], np.mean(meanakaproba_matrix, axis=1))
#
#file_exists = os.path.isfile("C:/Users/morga/Desktop/pyveea/Cleese/Heatmaps/FinalResults.csv")
#with open("C:/Users/morga/Desktop/pyveea/Cleese/Heatmaps/FinalResults.csv", mode='a', newline='') as file:
#    writer = csv.writer(file)
#
#    if not file_exists:
#        writer.writerow(['participant_id', 'comparison', 'spearman_coef', 'p_value'])
#
#    writer.writerow([101, 'delta_seg2_vs_response', spearman_seg2, p_value_seg2])
#    writer.writerow([101, 'delta_seg3_vs_response', spearman_seg3, p_value_seg3])


plt.xticks(np.linspace(0, chosen_interval, chosen_interval+1), x_range)
plt.yticks(np.linspace(0, chosen_interval, chosen_interval+1), y_range)
plt.title(str(CSV_name)+"'s heatmap")
plt.xlabel("Second half pitch")
plt.ylabel("First half pitch")
plt.show()
