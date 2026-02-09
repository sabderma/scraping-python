import requests

url = "https://www.google.com"
print("Requête vers", url)

r = requests.get(url, timeout=10)
print("Status:", r.status_code)
print("Longueur de la réponse:", len(r.text))
