from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Config navigateur
options = Options()
options.add_argument("--detach")
driver = webdriver.Chrome(options=options)
driver.get("https://www.boulanger.com/c/smartphone-telephone-portable#tr=smartphone")

# Accepter les cookies
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
    ).click()
except:
    print("Cookies déjà acceptés ou bouton non présent.")

# Attendre que les produits se chargent
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-list__item"))
)

results = driver.find_elements(By.CSS_SELECTOR, "li.product-list__item")

print(f"\n========== PAGE 1 ==========\n")
print(f"{len(results)} produits trouvés.\n")

# 🔹 Création du fichier CSV
with open("produits_boulanger.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # En-têtes du fichier
    writer.writerow(["Marque", "Titre", "Avis", "Prix"])

    for i, result in enumerate(results, 1):
        try:
            # Marque
            try:
                Marque = result.find_element(By.CSS_SELECTOR, "span.product-list__product-brand").text.strip()
            except NoSuchElementException:
                Marque = "Marque non disponible"

            # Titre
            try:
                Titre = result.find_element(By.CSS_SELECTOR, "h2.product-list__product-label").text.strip()
            except NoSuchElementException:
                Titre = "Titre non disponible"

            # Avis
            try:
                Avis = result.find_element(By.CSS_SELECTOR, "span.rating__count").text.strip()
            except NoSuchElementException:
                Avis = "Avis non disponible"

            # Prix
            try:
                price = result.find_element(By.CSS_SELECTOR, "p.price__amount").text.strip()
            except NoSuchElementException:
                price = "Prix non disponible"

            print(f"{i}. {Marque}\n  Titre: {Titre}\n  Avis: {Avis}\n  Prix: {price}\n")

            
            writer.writerow([Marque, Titre, Avis, price])

        except Exception as e:
            print(f"Erreur produit {i}: {e}")

driver.quit()
print("\nScraping terminé ✅ — les données ont été enregistrées dans 'produits_boulanger.csv'.")
