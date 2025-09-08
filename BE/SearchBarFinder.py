import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

CORRIERE = "https://www.corriere.it/ricerca/?q="


def trova_url_ricerca(dominio):
    dominio = 'https://'+dominio

    if "corriere.it" in dominio:
        return CORRIERE

    def analizza_html(html, base_url):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            for form in soup.find_all('form'):
                for input_tag in form.find_all('input'):
                    tipo = input_tag.get('type', '').lower()
                    nome = input_tag.get('name')
                    if tipo in ['search', 'text'] and nome:
                        action = form.get('action', '')
                        full_url = urljoin(base_url, action)
                        return f"{full_url}?{nome}="
            return [
                f"{full_url}?s=TUA_QUERY",
                f"{full_url}/ricerca?query=TUA_QUERY",
                f"{full_url}/ricerca?query=TUA_QUERY",
                f"{full_url}?search=TUA_QUERY",
                f"{full_url}/cerca?s=TUA_QUERY",
            ]
        except:
            return [
                f"{full_url}?s=TUA_QUERY",
                f"{full_url}/ricerca?query=TUA_QUERY",
                f"{full_url}/ricerca?query=TUA_QUERY",
                f"{full_url}?search=TUA_QUERY",
                f"{full_url}/cerca?s=TUA_QUERY",
            ]

    # Provo prima con requests (se form già visibile)
    try:
        resp = requests.get(dominio, timeout=10)
        risultato = analizza_html(resp.text, dominio)
        if risultato:
            return risultato
    except:
        pass

    # Selenium con gestione popup cookie e click bottone ricerca (anche icona)
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.get(dominio)
        wait = WebDriverWait(driver, 15)

        # Gestione popup cookie: cerca e clicca bottoni di accettazione comuni
        accetta_testi = ['accetta', 'consenti', 'ok',
                         'chiudi', 'accept', 'consent', 'close']
        buttons = driver.find_elements(
            By.TAG_NAME, "button") + driver.find_elements(By.TAG_NAME, "a")
        for btn in buttons:
            try:
                testo = (btn.text or "").strip().lower()
                if any(parola in testo for parola in accetta_testi) and btn.is_displayed() and btn.is_enabled():
                    btn.click()
                    time.sleep(2)  # attesa popup scompaia
                    break
            except:
                continue

        # Cerca e clicca bottone di ricerca, anche se è solo icona
        candidati = driver.find_elements(
            By.CSS_SELECTOR, "button, a, div, span")
        for el in candidati:
            try:
                if not el.is_displayed() or not el.is_enabled():
                    continue
                testo = (el.text or "").lower()
                aria = (el.get_attribute("aria-label") or "").lower()
                classes = (el.get_attribute("class") or "").lower()

                if ("search" in testo or "cerca" in testo or
                    "search" in aria or "cerca" in aria or
                        "search" in classes or "cerca" in classes):
                    el.click()
                    time.sleep(1)  # attesa animazione
                    break
            except:
                continue

        html = driver.page_source
        driver.quit()
        return analizza_html(html, dominio)
    except Exception as e:
        return e


if __name__ == "__main__":
    print(trova_url_ricerca("ilfattoquotidiano.it"))
    print(trova_url_ricerca("lastampa.it"))
    print(trova_url_ricerca("corriere.it"))
    print(trova_url_ricerca("www.repubblica.it"))
    print(trova_url_ricerca("www.ilpost.it"))
    print(trova_url_ricerca("www.secoloditalia.it"))
    print(trova_url_ricerca("www.oggi.it"))

    print(trova_url_ricerca("www.dagospia.com"))
    print(trova_url_ricerca("www.fanpage.it"))
    # print(trova_url_ricerca("www.leggo.it")) # Richiede iscrizione al sito
    print(trova_url_ricerca("nytimes.com"))  # Funziona alternativamente
