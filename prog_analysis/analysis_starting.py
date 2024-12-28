import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import csv


def response_time(file):
    
def generate_heatmap(df, output_path, num_participant):
    df['delta_seg2'] = df['stimuli_2_seg2'].astype(float) - df['stimuli_1_seg2'].astype(float)
    df['delta_seg3'] = df['stimuli_2_seg3'].astype(float) - df['stimuli_1_seg3'].astype(float)

    heatmap_data = df.pivot_table(
        values='response',
        index='delta_seg2',
        columns='delta_seg3',
        aggfunc='mean'
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(f"Participant {num_participant} - Heatmap of Responses")
    plt.xlabel("Delta Segment 3")
    plt.ylabel("Delta Segment 2")
    heatmap_file = os.path.join(output_path, f"{num_participant}_heatmap.png")
    plt.savefig(heatmap_file)
    plt.show()


# faire pour les 4
def analyze_correlation(df, name_file_to_save, num_participant):
    df['delta_seg2'] = df['stimuli_2_seg2'].astype(float) - df['stimuli_1_seg2'].astype(float)
    df['delta_seg3'] = df['stimuli_2_seg3'].astype(float) - df['stimuli_1_seg3'].astype(float)

    # Calcul des coefficients de Spearman
    spearman_seg2, p_value_seg2 = spearmanr(df['delta_seg2'], df['response'])
    spearman_seg3, p_value_seg3 = spearmanr(df['delta_seg3'], df['response'])

    # Sauvegarde des résultats dans un fichier CSV
    file_exists = os.path.isfile(name_file_to_save)
    with open(name_file_to_save, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Écrire l'en-tête si le fichier est nouveau
        if not file_exists:
            writer.writerow(['participant_id', 'comparison', 'spearman_coef', 'p_value'])

        # Ajouter les résultats
        writer.writerow([num_participant, 'delta_seg2_vs_response', spearman_seg2, p_value_seg2])
        writer.writerow([num_participant, 'delta_seg3_vs_response', spearman_seg3, p_value_seg3])

    print(f"Results saved to {name_file_to_save}")


def main(num_participant, relative_path, name_file_to_save="results_analysis_coefficients.csv"):
    folder_stimulus_1 = os.path.join(relative_path, "stimulus_1")
    folder_stimulus_2 = os.path.join(relative_path, "stimulus_2")
    output_path = os.path.join(relative_path, "output")

    os.makedirs(output_path, exist_ok=True)

    participant_df = csv_maker_per_participant(num_participant, output_path, folder_stimulus_1, folder_stimulus_2)

    analyze_correlation(participant_df, name_file_to_save, num_participant)

    generate_heatmap(participant_df, output_path, num_participant)
