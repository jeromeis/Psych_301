import re
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import csv


# make the csv with |trial|S_I|S_III|Response (1 or 2) for each participants
def list_trial_computer(folder_stimulus_1, folder_stimulus_2):
    labels = ['trial', 'stimuli_1_seg2', 'stimuli_1_seg3', 'stimuli_2_seg2', 'stimuli_2_seg3']

    pattern = r"_p2at-(?P<value_p2>[0-9]+\.[0-9]+)_p3at-(?P<value_p3>[0-9]+\.[0-9]+)"

    trial = 1
    rows = []

    folder1_files = sorted(os.listdir(folder_stimulus_1))
    folder2_files = sorted(os.listdir(folder_stimulus_2))

    for doc1, doc2 in zip(folder1_files, folder2_files):
        doc1_path = os.path.join(folder_stimulus_1, doc1)
        doc2_path = os.path.join(folder_stimulus_2, doc2)

        # Extraction des valeurs à partir des fichiers
        s1_match = re.search(pattern, doc1)
        s2_match = re.search(pattern, doc2)

        if s1_match and s2_match:
            rows.append({
                'trial': trial,
                'stimuli_1_seg2': s1_match.group("value_p2"),
                'stimuli_1_seg3': s1_match.group("value_p3"),
                'stimuli_2_seg2': s2_match.group("value_p2"),
                'stimuli_2_seg3': s2_match.group("value_p3"),
            })
            trial += 1

    df = pd.DataFrame(rows, columns=labels)
    return df


# to do
def csv_maker_per_participant(num_participant, file_path, folder_stimulus_1, folder_stimulus_2):

    initial_df = list_trial_computer(folder_stimulus_1, folder_stimulus_2)
    initial_df = initial_df.sort_values('trial')



    final_df = ...

    name_file_to_save = f"{file_path}/{num_participant}_ready_for_analysis.csv"
    file = final_df.to_csv(name_file_to_save)

    return name_file_to_save


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
    plt.title("Heatmap des réponses en fonction des deltas")
    plt.xlabel("Delta Segment 3")
    plt.ylabel("Delta Segment 2")
    plt.savefig(os.path.join(output_path, f"{num_participant}_heatmap.png"))
    plt.show()


def main(num_participant, relative_path, name_file_to_save="results_analysis_coefficients.csv"):
    folder_stimulus_1 = os.path.join(relative_path, "stimulus_1")
    folder_stimulus_2 = os.path.join(relative_path, "stimulus_2")
    output_path = os.path.join(relative_path, "output")

    os.makedirs(output_path, exist_ok=True)

    participant_df = csv_maker_per_participant(num_participant, output_path, folder_stimulus_1, folder_stimulus_2)

    analyze_correlation(participant_df, name_file_to_save, num_participant)

    generate_heatmap(participant_df, output_path, num_participant)
