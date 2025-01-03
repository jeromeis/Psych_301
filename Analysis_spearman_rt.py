import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import csv


def response_time(df, num_participant, file_to_save="Response_time.csv"):
    filtered_response_times = df['response time'][df['response time'] <= 1000]
    average = filtered_response_times.mean()
    std = filtered_response_times.std()

    file_exists = os.path.isfile(file_to_save)
    with open(file_to_save, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['participant', 'average_rt', 'std_rt'])
        writer.writerow([num_participant, average, std])

    print(f"Results saved to {file_to_save}")


# Fonction pour générer la carte de chaleur
def generate_heatmap(df, output_path, num_participant):
    df['delta_seg2'] = df['P2\'-P2'].astype(float)
    df['delta_seg3'] = df['P3\'-P3'].astype(float)

    heatmap_data = df.pivot_table(
        values='decision',
        index='delta_seg2',
        columns='delta_seg3',
        aggfunc='mean'
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Probability of Decision 1'})
    plt.title(f"Participant {num_participant} - Heatmap of Responses")
    plt.xlabel("Delta Segment 3")
    plt.ylabel("Delta Segment 2")
    heatmap_file = os.path.join(output_path, f"{num_participant}_heatmap.png")
    plt.savefig(heatmap_file)
    plt.close()


# Fonction pour analyser les corrélations et les sauvegarder
def analyze_correlation(df, name_file_to_save, num_participant):
    deltas = ["P1\'-P1", "P2\'-P2", "P3\'-P3", "P4\'-P4"]
    correlations = []
    for delta in deltas:
        spearman_coef, p_value = spearmanr(df[delta], df['decision'])
        correlations.append([num_participant, delta, spearman_coef, p_value])

    file_exists = os.path.isfile(name_file_to_save)
    with open(name_file_to_save, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['participant_id', 'delta', 'spearman_coef', 'p_value'])
        writer.writerows(correlations)

    print(f"Correlation results saved to {name_file_to_save}")

# Fonction principale pour orchestrer l'analyse
def main():
    name_file_to_save_coef = "results_analysis_coefficients.csv"

    folder_path = "final_data_csv"

    output_path = "output_analysis"
    os.makedirs(output_path, exist_ok=True)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):

            file_no_csv, extension = file_name.split(".")
            parts = file_no_csv.split('_')

            num_participant = parts[3]
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            
            required_columns = ["P1\'-P1", "P2\'-P2", "P3\'-P3", "P4\'-P4", "decision", "response time"]
            if not all(col in df.columns for col in required_columns):
                print(f"The file {file_name} is missing required columns.")
                continue

            df["P1\'-P1"] = round(df["P1\'-P1"], 2)
            df["P2\'-P2"] = round(df["P2\'-P2"], 2)
            df["P3\'-P3"] = round(df["P3\'-P3"], 2)
            df["P4\'-P4"] = round(df["P4\'-P4"], 2)
            analyze_correlation(df, name_file_to_save_coef, num_participant)
            generate_heatmap(df, output_path, num_participant)
            response_time(df, num_participant, file_to_save="Response_time.csv")


if __name__ == "__main__":
    main()
