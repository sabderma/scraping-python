from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv

# Config navigateur
options = Options()
options.add_argument("--detach")
driver = webdriver.Chrome(options=options)

driver.get("https://www.amazon.fr/s?k=smartphone&crid=3K12222HFT3RH&sprefix=sm%2Caps%2C58&ref=nb_sb_ss_mvt-t11-ranker_1_2")

# Accepter les cookies
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
    ).click()
except:
    print("Cookies déjà acceptés ou bouton non présent.")

product_selector = "div.s-result-item[data-asin][data-component-type='s-search-result']"

#  Création du fichier CSV
with open("produits_amazon.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Titre", "Avis", "Prix"])

    page = 1

    while page < 10:
        print(f"\n========== PAGE {page} ==========\n")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, product_selector))
            )
        except TimeoutException:
            print(" Aucun produit détecté, fin du scraping.")
            break

        results = driver.find_elements(By.CSS_SELECTOR, product_selector)
        print(f"{len(results)} produits trouvés.\n")

        for i, result in enumerate(results, 1):
            try:
                # Titre
                try:
                    Titre = result.find_element(By.CSS_SELECTOR,
                        "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal"
                    ).text.strip()
                except NoSuchElementException:
                    Titre = "Titre non disponible"

                # Avis
                try:
                    Avis = result.find_element(By.CSS_SELECTOR,
                        "span.a-size-mini.puis-normal-weight-text.s-underline-text"
                    ).text.strip()
                except NoSuchElementException:
                    Avis = "Avis non disponible"

                # Prix 
                try:
                    whole = result.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
                    fraction = result.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text.strip()
                    price = f"{whole},{fraction}€"
                except NoSuchElementException:
                    price = "Prix non disponible"

                print(f"{i}.  Titre: {Titre}\n  Avis: {Avis}\n  Prix: {price}\n")
                writer.writerow([page, Titre, Avis, price])

            except Exception as e:
                print(f"Erreur produit {i}: {e}")

        # --- Pagination : bouton Suivant ---
        try:
            next_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-item.s-pagination-next"))
            )

          

            next_btn.click()
            page += 1
            time.sleep(3)

        except TimeoutException:
            print(" Plus de pages à parcourir (bouton Suivant introuvable).")
            break

driver.quit()
print("\nScraping terminé — toutes les pages ont été enregistrées dans 'produits_amazon.csv'.")




