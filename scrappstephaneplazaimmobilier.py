from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv, time, re

# ------------------ Config navigateur ------------------
options = Options()
options.add_argument("--detach")     # retire si tu ne veux pas garder la fenêtre ouverte
driver = webdriver.Chrome(options=options)

url = "https://www.stephaneplazaimmobilier.com/acheter/departement/paris_75/appartement,maison/"
driver.get(url)

# ------------------ Cookies ------------------
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "tarteaucitronPersonalize2"))
    ).click()
except Exception:
    print("Cookies déjà acceptés ou bouton non présent.")

# ------------------ Scroll pour TOUT charger ------------------
prev = -1
while True:
    cards = driver.find_elements(By.CSS_SELECTOR, "div.room.purchase")
    if len(cards) == prev:
        print(f"✅ Fin du scroll : {len(cards)} annonces détectées.")
        break
    print(f"📦 Annonces visibles : {len(cards)} — on scrolle…")
    prev = len(cards)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

# ------------------ Scrape & CSV ------------------
with open("annonces_plaza_paris.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["type", "prix", "surface", "nb_pieces", "localisation", "details"])

    cards = driver.find_elements(By.CSS_SELECTOR, "div.room.purchase")
    print(f"\n🔎 Total final : {len(cards)} cartes à parser\n")

    for i, card in enumerate(cards, 1):
        type_bien = "non disponible"
        prix = "non disponible"
        surface = "non disponible"
        nb_pieces = "non disponible"
        localisation = "non disponible"
        details = "non disponible"

        # ---- PRIX (span.card-right) ----
        try:
            txt = card.find_element(By.CSS_SELECTOR, "span.card-right").text.strip()
            if txt:
                prix = txt
        except NoSuchElementException:
            pass

        # ---- LOCALISATION (span.card-left.uppercase) ----
        try:
            txt = card.find_element(By.CSS_SELECTOR, "span.card-left.uppercase").text.strip()
            if txt:
                localisation = txt
        except NoSuchElementException:
            pass

        # ---- TITRE (h3.title-wrap) pour type/surface/pièces ----
        titre = ""
        try:
            titre = card.find_element(By.CSS_SELECTOR, "h3.title-wrap").text.strip()
        except NoSuchElementException:
            pass

        bloc_txt = titre or card.text  # fallback robuste

        # type
        if re.search(r"appartement", bloc_txt, re.I):
            type_bien = "Appartement"
        elif re.search(r"maison", bloc_txt, re.I):
            type_bien = "Maison"

        # nb pièces
        m = re.search(r"(\d+)\s*pi[eè]ce", bloc_txt, re.I)
        if m:
            nb_pieces = f"{m.group(1)} pièces"

        # surface (gère virgule/point)
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*m(?:²|2)", bloc_txt, re.I)
        if m:
            surface = f"{m.group(1).replace(',', '.')} m²"

        # ---- DÉTAILS (premier <p> descriptif) ----
        try:
            p = card.find_element(By.CSS_SELECTOR, "p")
            txt = p.text.strip()
            if txt:
                details = txt
        except NoSuchElementException:
            pass

        print(f"{i}. {type_bien} | {prix} | {surface} | {nb_pieces} | {localisation} | {details[:80]}{'…' if len(details)>80 else ''}")
        writer.writerow([type_bien, prix, surface, nb_pieces, localisation, details])

print("\n✅ Scraping terminé — toutes les annonces chargées et exportées dans 'annonces_plaza_paris.csv'.")
driver.quit()
