import scipy.io
import pandas as pd
import os
import numpy as np

def load_and_merge_mat_files_from_folder(folder_path, label_column_name):
    """
    Fusionne les fichiers MATLAB dans un dossier en regroupant les lignes par label.
    """
    all_data = []

    # Vérifier si le dossier existe
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier spécifié n'existe pas : {folder_path}")

    # Liste tous les fichiers .mat dans le dossier
    mat_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mat')]

    if len(mat_files) == 0:
        raise ValueError("Aucun fichier .mat trouvé dans le dossier spécifié.")

    # Charger chaque fichier MATLAB
    for file in mat_files:
        try:
            mat_data = scipy.io.loadmat(file)

            # Trouver les clés de données (ignorer les métadonnées)
            data_key = [key for key in mat_data.keys() if not key.startswith("__")]
            if not data_key:
                raise ValueError(f"Aucune donnée valide trouvée dans le fichier {file}.")

            # Utiliser la première clé de données
            key = data_key[0]
            data = mat_data[key]

            # Vérifier que 'data' est bien sous forme de tableau
            if not isinstance(data, (list, np.ndarray)):
                raise ValueError(f"Les données du fichier {file} ne sont pas dans un format attendu.")

            # Convertir en DataFrame
            df = pd.DataFrame(data)

            # Renommer les colonnes pour correspondre à 'trial', 'decision', 'response time'
            # Supposons que les colonnes du fichier .mat soient dans le même ordre
            # ou qu'elles aient des noms similaires. Vous pouvez ajuster en fonction de la structure des données.
            if df.shape[1] == 3:
                df.columns = ['trial', 'decision', 'response time']
            else:
                raise ValueError(f"Le fichier {file} ne contient pas 3 colonnes attendues.")
            
            # Ajouter une colonne pour identifier le fichier trial
            df['Trial_File'] = os.path.basename(file)

            # Ajouter les données au tableau global
            all_data.append(df)
        except Exception as e:
            print(f"Erreur lors du traitement du fichier {file} : {e}")

    # Concaténer tous les fichiers en un DataFrame unique
    merged_df = pd.concat(all_data, ignore_index=True)

    # Trier les données pour regrouper les lignes avec les mêmes labels
    if label_column_name in merged_df.columns:
        merged_df = merged_df.sort_values(by=label_column_name)
    else:
        raise ValueError(f"La colonne de labels '{label_column_name}' est introuvable dans les données fusionnées.")

    return merged_df


def add_stimuli_data(merged_df, stimuli_path, label_column_name):
    """
    Intègre les colonnes d'un fichier Excel ou ODS dans le DataFrame fusionné.
    """
    file_extension = os.path.splitext(stimuli_path)[1].lower()
    try:
        # Charger les données stimuli
        if file_extension == ".ods":
            stimuli_data = pd.read_excel(stimuli_path, engine="odf")
        elif file_extension in [".xlsx", ".xls"]:
            stimuli_data = pd.read_excel(stimuli_path)
        else:
            raise ValueError(f"Format de fichier non pris en charge : {file_extension}")

        # Vérifier que la colonne de labels existe dans stimuli
        if label_column_name not in stimuli_data.columns:
            raise ValueError(f"Colonne '{label_column_name}' introuvable dans le fichier stimuli.")

        # Vérifier que la colonne de labels existe également dans merged_df
        if label_column_name not in merged_df.columns:
            raise ValueError(f"Colonne '{label_column_name}' introuvable dans les données fusionnées.")

        # Fusionner les données sur la colonne de labels
        enriched_df = pd.merge(merged_df, stimuli_data, on=label_column_name, how='left')
        return enriched_df
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'ajout des données stimuli : {e}")


def save_merged_data_to_csv(merged_df, output_path):
    """
    Sauvegarde les données fusionnées dans un fichier CSV.
    """
    try:
        # Ajouter l'encodage utf-8 lors de la sauvegarde pour éviter les problèmes avec les caractères spéciaux
        merged_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Les données fusionnées ont été sauvegardées dans : {output_path}")
    except Exception as e:
        raise IOError(f"Erreur lors de la sauvegarde du fichier : {e}")


def main(folder_matlab="Results"):
    folder_path = folder_matlab.strip()  # Chemin du dossier Results
    stimuli_path = "stimuli_values.ods"  # Chemin vers stimuli_values
    participant_id = input("Entrez le numéro du participant : ").strip()

    if not participant_id.isdigit():
        raise ValueError("Le numéro du participant doit être un entier positif.")

    label_column_name = "trial"
    output_path = f"merged_data_participant_{participant_id}.csv"

    # Fusionner les fichiers MATLAB
    merged_df = load_and_merge_mat_files_from_folder(folder_path, label_column_name)

    # Ajouter les données stimuli
    merged_df = add_stimuli_data(merged_df, stimuli_path, label_column_name)

    # Sauvegarder les données fusionnées
    save_merged_data_to_csv(merged_df, output_path)


if __name__ == "__main__":
    try:
        folder_matlab = input("Quel est le chemin ou le nom du dossier contenant les fichiers MATLAB ? (par défaut : 'Results') : ").strip()
        if not folder_matlab:
            folder_matlab = "Results"
        main(folder_matlab)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")