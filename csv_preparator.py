import scipy.io
import pandas as pd
import os

def load_and_merge_mat_files_from_folder(folder_path, label_column_name):
    """
    Fusionne les fichiers MATLAB dans un dossier en regroupant les lignes par label.
    :param folder_path: Chemin du dossier contenant les fichiers .mat
    :param label_column_name: Nom de la colonne contenant les labels
    :return: DataFrame fusionné
    """
    all_data = []

    # Liste tous les fichiers .mat dans le dossier
    mat_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.mat')]

    if len(mat_files) == 0:
        raise ValueError("Aucun fichier .mat trouvé dans le dossier spécifié.")

    # Charger chaque fichier MATLAB
    for file in mat_files:
        mat_data = scipy.io.loadmat(file)

        # Trouver les clés de données (ignorer les métadonnées)
        data_key = [key for key in mat_data.keys() if not key.startswith("__")]
        if not data_key:
            raise ValueError(f"Aucune donnée valide trouvée dans le fichier {file}.")

        # Utiliser la première clé de données
        key = data_key[0]
        data = mat_data[key]

        # Convertir en DataFrame
        df = pd.DataFrame(data)

        # Renommer les colonnes si nécessaire (assurez-vous que les colonnes ont des noms)
        df.columns = [f"col_{i}" for i in range(df.shape[1])]

        # Vérifiez que la colonne des labels existe
        if label_column_name not in df.columns:
            raise ValueError(f"Colonne '{label_column_name}' introuvable dans le fichier {file}.")

        # Ajouter les données au tableau global
        all_data.append(df)

    # Concaténer tous les fichiers en un DataFrame unique
    merged_df = pd.concat(all_data)

    # Trier les données pour regrouper les lignes avec les mêmes labels
    merged_df = merged_df.sort_values(by=label_column_name)

    return merged_df


def add_excel_data(merged_df, excel_path, label_column_name):
    """
    Intègre les colonnes d'un fichier Excel ou ODS dans le DataFrame fusionné.
    :param merged_df: DataFrame fusionné.
    :param excel_path: Chemin du fichier Excel ou ODS contenant les données supplémentaires.
    :param label_column_name: Nom de la colonne de labels pour effectuer la jointure.
    :return: DataFrame enrichi avec les colonnes provenant de l'Excel/ODS.
    """
    # Charger les données Excel ou ODS avec le moteur approprié
    file_extension = os.path.splitext(excel_path)[1].lower()
    if file_extension == ".ods":
        excel_data = pd.read_excel(excel_path, engine="odf")
    elif file_extension == ".xlsx" or file_extension == ".xls":
        excel_data = pd.read_excel(excel_path)
    else:
        raise ValueError(f"Format de fichier non pris en charge : {file_extension}")

    # Vérifiez que la colonne de labels existe dans l'Excel
    if label_column_name not in excel_data.columns:
        raise ValueError(f"Colonne '{label_column_name}' introuvable dans le fichier Excel/ODS.")

    # Fusionner les données sur la colonne de labels
    enriched_df = pd.merge(merged_df, excel_data, on=label_column_name, how='left')

    return enriched_df


def save_merged_data_to_csv(merged_df, output_path):
    """
    Sauvegarde les données fusionnées dans un fichier CSV.
    :param merged_df: DataFrame fusionné
    :param output_path: Chemin pour sauvegarder le fichier CSV
    """
    merged_df.to_csv(output_path, index=False)
    print(f"Data merged and saved to {output_path}")


def main():
    folder_path = input("Entrez le chemin du dossier contenant les fichiers .mat : ").strip()
    excel_path = "stimuli_values.ods"
    participant_id = input("Entrez le numéro du participant : ").strip()

    if not participant_id.isdigit():
        raise ValueError("Le numéro du participant doit être un entier positif.")

    label_column_name = "col_0"  # Remplacez par le nom de la colonne de labels
    output_path = f"merged_data_participant_{participant_id}.csv"  # Nom du fichier avec numéro du participant

    # Fusionner les fichiers du dossier
    merged_df = load_and_merge_mat_files_from_folder(folder_path, label_column_name)

    # Ajouter les données Excel ou ODS
    merged_df = add_excel_data(merged_df, excel_path, label_column_name)

    # Sauvegarder les données fusionnées
    save_merged_data_to_csv(merged_df, output_path)


if __name__ == "__main__":
    main()
