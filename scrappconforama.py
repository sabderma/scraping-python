from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv


options = Options()
options.add_argument("--detach")
driver = webdriver.Chrome(options=options)

BASE = "https://www.conforama.fr/recherche-conforama/smartphone?fromSearch=smartphone"
MAX_PAGES = 5   

with open("produits_conforama.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Titre", "Avis", "Prix"])


    for page in range(1, MAX_PAGES + 1):
        url = BASE if page == 1 else f"{BASE}&p={page}"
        driver.get(url)
        print(f"\n========== PAGE {page} ==========\n")

        if page == 1:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                ).click()
            except:
                print("Cookies déjà acceptés ou bouton non présent.")

   
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[data-component-id='product-tile']"))
        )

        results = driver.find_elements(By.CSS_SELECTOR, "article[data-component-id='product-tile']")

        print(f"{len(results)} produits trouvés sur la page {page}.\n")

        for i, result in enumerate(results, 1):
            try:
              

                # Titre
                try:
                     Titre = result.find_element(By.CSS_SELECTOR, 'a[data-component-id="product-tile-product-name"]').text.strip()
                except NoSuchElementException:
                    Titre = "Titre non disponible"

                # Avis
                try:
                    Avis = result.find_element(By.CSS_SELECTOR, "div.font-normal").text.strip()
                except NoSuchElementException:
                    Avis = "Avis non disponible"

                # Prix
                try:
                    price = result.find_element(By.CSS_SELECTOR,"span.font-bold.text-2xl.text-black").text
                except NoSuchElementException:
                    price = "Prix non disponible"

                print(f"{i}.Titre: {Titre}\n  Avis: {Avis}\n  Prix: {price}\n")
                writer.writerow([page, Titre, Avis, price])

            except Exception as e:
                print(f"Erreur produit {i}: {e}")

        time.sleep(2)  # pause entre pages

driver.quit()
print("\n Scraping terminé — les données ont été enregistrées dans 'produits_conforama.csv'.")
