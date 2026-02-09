import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("produits_boulanger.csv")

# --- 1 Supprimer les espaces inutiles dans les colonnes ---
df.columns = df.columns.str.strip()

# --- 2 Nettoyer les valeurs texte (espaces, caractères spéciaux inutiles) ---
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# --- 3 Nettoyer la colonne "Prix" ---
# Supprimer le signe €, remplacer la virgule par un point et convertir en float
df["Prix"] = (
    df["Prix"]
    .str.replace("€", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.replace(" ", "", regex=False)
    .astype(float)
)

# --- 4 Nettoyer la colonne "Avis" ---
# Supprimer les parenthèses et convertir en nombre (NaN si pas d'avis)
df["Avis"] = (
    df["Avis"]
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
    .str.replace("Avis non disponible", "", regex=False)
    .replace("", pd.NA)
)
df["Avis"] = pd.to_numeric(df["Avis"], errors="coerce")

# --- 5 Supprimer les doublons s’il y en a ---
df = df.drop_duplicates()

# --- 6 Supprimer les lignes vides éventuelles ---
df = df.dropna(subset=["Titre", "Marque"])

# --- 7 Trier les produits par prix décroissant ---
df = df.sort_values(by="Prix", ascending=False)

# --- 8 Réinitialiser l’index ---
df = df.reset_index(drop=True)

# --- 9 Sauvegarder le fichier nettoyé ---
df.to_csv("produits_boulanger_clean.csv", index=False)

# ---  10 Afficher un aperçu ---
print(df.head())
print("\nInfos sur le DataFrame nettoyé :")
print(df.info())
