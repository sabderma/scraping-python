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

BASE = "https://www.electrodepot.fr/smartphone-mobilite/smartphone-telephone/smartphone.html?q=smartphone"
driver.get(BASE)

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "accept-recommended-btn-handler"))
    ).click()
except:
    print("Cookies déjà acceptés ou bouton non présent.")

with open("produits_boulanger.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Marque", "Titre", "Avis", "Prix"])

    MAX_PAGES = 5   
    for page in range(1, MAX_PAGES + 1):
        url = BASE if page == 1 else f"{BASE}&page={page}"
        driver.get(url)
        print(f"\n========== PAGE {page} ==========\n")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.productlist-item_block"))
            )
        except:
            print(" Aucun produit détecté (sélecteur non trouvé).")
            continue

        results = driver.find_elements(By.CSS_SELECTOR, "div.productlist-item_block")
        print(f"{len(results)} produits trouvés.\n")

        for i, result in enumerate(results, 1):
            try:
                # Marque
                try:
                    Marque = result.find_element(By.CSS_SELECTOR, "div.productlist-item--brand").text.strip()
                except NoSuchElementException:
                    Marque = "Marque non disponible"

                # Titre
                try:
                    Titre = result.find_element(By.CSS_SELECTOR, "h2.productlist-item--name").text.strip()
                except NoSuchElementException:
                    Titre = "Titre non disponible"

                # Avis
                try:
                    Avis = result.find_element(By.CSS_SELECTOR, "span.nombre-avis").text.strip()
                except NoSuchElementException:
                    Avis = "Avis non disponible"

                # Prix
                try:
                    price = result.find_element(By.CSS_SELECTOR, "div.number_price").text.strip()
                except NoSuchElementException:
                    price = "Prix non disponible"

                print(f"{i}. {Marque}\n  Titre: {Titre}\n  Avis: {Avis}\n  Prix: {price}\n")
                writer.writerow([Marque, Titre, Avis, price])

            except Exception as e:
                print(f"Erreur produit {i}: {e}")

        time.sleep(2) 

driver.quit()
print("\nScraping terminé  — les données ont été enregistrées dans 'produits_boulanger.csv'.")
