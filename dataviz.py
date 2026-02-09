import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv("produits_boulanger_clean.csv")


# --- 1. Histogramme : Répartition des produits par marque ---
plt.figure(figsize=(8, 5))
plt.hist(df['Marque'], bins=len(df['Marque'].unique()), color="green", edgecolor="black")
plt.title("Répartition des produits par marque")
plt.xlabel("Marques")
plt.ylabel("Fréquence (nombre de produits)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# --- 2. Graphique : Prix moyen par marque ---
prix_moyen = df.groupby('Marque')['Prix'].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(prix_moyen.index, prix_moyen.values, color="orange", edgecolor="black")
plt.title("Prix moyen par marque", fontsize=14)
plt.xlabel("Marques", fontsize=12)
plt.ylabel("Prix moyen (€)", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# === 3 Répartition du prix par marque (Boxplot) ===
plt.figure(figsize=(10, 6))
sns.boxplot(x='Marque', y='Prix', data=df, palette="Set2")

plt.title("Distribution des prix par marque", fontsize=14)
plt.xlabel("Marque", fontsize=12)
plt.ylabel("Prix (€)", fontsize=12)
plt.xticks(rotation=45, ha="right")

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()