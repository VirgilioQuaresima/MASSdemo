"""Esempio di utilizzo delle funzioni di ricerca e analisi
   per estrarre dati da Google API, Firecrawl e ChatGPT."""

from datetime import datetime
import json
import random
from BE.chatGPT_analysis import analysis
from BE.firecrawl_search import main as firecrawl_main
from BE.google_api_search import search_query, search_image_query
from BE.SearchBarFinder import trova_url_ricerca


# 1. Estrazione dati da Google API
# 2. Estrazione di sito ricerca
# 3. Estrazione dei contenuti da sito con firecrawl
# 4. Analisi del sentiment con ChatGPT


def demo(full_name: str, domain: str)-> dict:
    """Funzione di esempio per dimostrare l'uso delle funzioni di ricerca e analisi."""

################################################################################
    # Estrazione dati da Google API

    search_results = search_query(full_name, domain)
    domain_name = domain.split('.')[0]
    if not search_results or len(search_results) == 0:
        print("Nessun risultato trovato su Google API.")

    print(f"Risultati di ricerca per '{full_name}' su {domain}:")
    # for result in search_results:
    #     print(f"Titolo: {result['title']}, Link: {result['url']}")
    print("\nEseguo ricerca immagini...")
    image_results = search_image_query(full_name, domain)
    if not image_results or len(image_results) == 0:
        print("Nessuna immagine trovata su Google API.")
    print(f"Risultati di ricerca immagini per '{full_name}' su {domain}:")
    for el in search_results:
        el['sentiment'] = ""
        el['summary'] = ""
        el['phrase'] = ""
    for el in image_results:
        el['sentiment'] = ""
        el['summary'] = ""
        el['phrase'] = ""

    urla = [el['url'] for el in search_results]
    for el in image_results:
        if el['url'] not in urla:
            search_results.append(el)

    file_json = {
        "name": full_name,
        "domain": domain,
        "results": search_results,
    }

    with open(f"google/google_api_results_{full_name}_{domain_name}.json", "w") as f:
        json.dump(file_json, f, indent=4)

    random_index_list = [random.randint(
        0, len(search_results)-1) for _ in range(10)]
    chat_analysis_results = [search_results[i]['url']
                             for i in random_index_list]
    final = [search_results[i] for i in random_index_list]

    # for image in image_results:
    #     print(f"Titolo: {image['title']}, Link: {image['url']}")

################################################################################
    # Estrazione di sito ricerca

    # print("\nEseguo ricerca URL di ricerca...")
    # search_url = trova_url_ricerca(domain)
    # if not search_url:
    #     print("Nessun URL di ricerca trovato.")
    #     return
    # print(f"URL di ricerca trovato: {search_url}")

################################################################################
    # Estrazione dei contenuti da sito con firecrawl

    # print("\nEseguo ricerca contenuti con Firecrawl...")
    # firecrawl_results = firecrawl_main(full_name, domain, search_url) or []
    # if not firecrawl_results or len(firecrawl_results) == 0:
    #     print("Nessun contenuto trovato con Firecrawl.")
    # print(f"Contenuti trovati su {domain}:")
    # for content in firecrawl_results:
    #     print(f"Titolo: {content['title']}, URL: {content['url']}")

    # if firecrawl_results and len(firecrawl_results) > 0:
    #     chat_analysis_results = chat_analysis_results + \
    #         [firecrawl_results[i]['url'] for i in range(3)]

################################################################################
    # Analisi del sentiment con ChatGPT

    print("\nEseguo analisi del sentiment con ChatGPT...")
    analysis_results = analysis(full_name,
                                chat_analysis_results)

    if not analysis_results or len(analysis_results) == 0:
        print("Nessun risultato di analisi del sentiment trovato.")
        return
    for el in final:
        el['sentiment'] = analysis_results[final.index(el)]['sentiment']
        el['summary'] = analysis_results[final.index(el)]['summary']
        el['phrase'] = analysis_results[final.index(el)]['phrase']

    with open(f"gpt/chatgpt_analysis_{full_name}_{domain_name}.json", "w") as f:
        json.dump(analysis_results, f, indent=4)

    final_urla = [el['url'] for el in final]

    for el in search_results:
        if el['url'] in final_urla:
            el['sentiment'] = final[final_urla.index(
                el['url'])]['sentiment']
            el['summary'] = final[final_urla.index(
                el['url'])]['summary']
            el['phrase'] = final[final_urla.index(
                el['url'])]['phrase']

    stamp_json = {
        "name": full_name,
        "domain": domain,
        "search_date": datetime.today().strftime('%d-%m-%Y'),
        "results": search_results,
    }
    with open(f"full/final_results_{full_name}_{domain_name}.json", "w") as f:
        json.dump(stamp_json, f, indent=4)
    
    return stamp_json
    # print("Risultati dell'analisi del sentiment:")
    # i = -1
    # for result in analysis_results:
    #     i += 1
    #     print(
    #         f"Titolo: {chat_analysis_results[i]['title']}, Sentiment: {result['sentiment']}")


# if __name__ == "__main__":

#     lista_test = [
#         ('Kanye West', 'corriere.it'),
#         # ('Donald Trump', 'repubblica.it'),
#         # ('Donald Trump', 'lastampa.it'),
#         #  ('Kanye West', 'ilsole24ore.com'),
#         #  ('Kanye West', 'ilfattoquotidiano.it'),
#         #  ('Donald Trump', 'ilmessaggero.it'),
#         #  ('Kanye West', 'ilgiornale.it'),
#         #  ('Elon Musk', 'lanazione.it'),
#         #  ('Donald Trump', 'ilrestodelcarlino.it'),
#         #  ('Donald Trump', 'ilmattino.it'),
#         #  ('Elon Musk', 'secoloxix.it'),
#         #  ('Donald Trump', 'ilgazzettino.it'),
#         #  ('Elon Musk', 'avvenire.it'),
#         #  ('Donald Trump', 'liberoquotidiano.it'),
#         #  ('Donald Trump', 'ilfoglio.it'),
#         #  ('Kanye West', 'ilmanifesto.it'),
#         #  ('Kanye West', 'ansa.it'),
#         #  ('Elon Musk', 'agi.it'),
#         #  ('Elon Musk', 'adnkronos.com'),
#         #  ('Elon Musk', 'gazzetta.it'),
#         #  ('Kanye West', 'nytimes.com'),
#         #  ('Kanye West', 'washingtonpost.com'),
#         #  ('Kanye West', 'wsj.com'),
#         #  ('Kanye West', 'usatoday.com'),
#         #  ('Donald Trump', 'latimes.com'),
#         #  ('Elon Musk', 'chicagotribune.com'),
#         #  ('Donald Trump', 'bostonglobe.com'),
#         #  ('Donald Trump', 'sfchronicle.com'),
#         # ('Elon Musk', 'npr.org'),
#         #  ('Donald Trump', 'cnn.com'),
#         #  ('Donald Trump', 'foxnews.com'),
#         #  ('Donald Trump', 'nbcnews.com'),
#         #  ('Donald Trump', 'abcnews.go.com'),
#         #  ('Kanye West', 'cbsnews.com'),
#         #  ('Elon Musk', 'bloomberg.com'),
#         #  ('Donald Trump', 'politico.com'),
#         # ('Donald Trump', 'theatlantic.com'),
#         #  ('Elon Musk', 'time.com'),
#         #  ('Elon Musk', 'apnews.com'),
#         #  ('Elon Musk', 'vox.com'),
#         #  ('Elon Musk', 'kommersant.ru'),
#         #  ('Elon Musk', 'rbc.ru'),
#         #  ('Elon Musk', 'chinadaily.com.cn'),
#         #  ('Kanye West', 'xinhuanet.com'),
#         #  ('Donald Trump', 'japantimes.co.jp'),
#         #  ('Kanye West', 'asahi.com'),
#         #  ('Donald Trump', 'timesofindia.indiatimes.com'),
#         #  ('Elon Musk', 'thehindu.com'),
#         #  ('Donald Trump', 'bbc.com'),
#         #  ('Elon Musk', 'theguardian.com'),
#         #  ('Elon Musk', 'telegraph.co.uk'),
#         #  ('Elon Musk', 'lemonde.fr'),
#         #  ('Kanye West', 'lefigaro.fr'),
#         #  ('Elon Musk', 'spiegel.de'),
#         #  ('Donald Trump', 'zeit.de'),
#         #  ('Kanye West', 'elpais.com'),
#         #  ('Elon Musk', 'elmundo.es'),
#         #  ('Donald Trump', 'publico.pt'),
#         #  ('Donald Trump', 'nrc.nl'),
#         #  ('Elon Musk', 'lesoir.be'),
#         #  ('Kanye West', 'nzz.ch'),
#         #  ('Donald Trump', 'orf.at'),
#         #  ('Donald Trump', 'irishtimes.com'),
#         #  ('Kanye West', 'dn.se'),
#         #  ('Elon Musk', 'aftenposten.no'),
#         #  ('Elon Musk', 'wyborcza.pl'),
#         #  ('Donald Trump', 'ekathimerini.com'),
#         #  ('Donald Trump', 'hurriyet.com.tr'),
#         #  ('Kanye West', 'kyivpost.com'),
#         #  ('Kanye West', 'theglobeandmail.com'),
#         #  ('Donald Trump', 'cbc.ca'),
#         #  ('Elon Musk', 'eluniversal.com.mx'),
#         #  ('Donald Trump', 'globo.com'),
#         #  ('Elon Musk', 'estadao.com.br'),
#         #  ('Kanye West', 'clarin.com'),
#         #  ('Elon Musk', 'emol.com'),
#         #  ('Donald Trump', 'eltiempo.com'),
#         #  ('Kanye West', 'haaretz.com'),
#         #  ('Elon Musk', 'aljazeera.com'),
#         #  ('Donald Trump', 'thenationalnews.com'),
#         #  ('Kanye West', 'arabnews.com'),
#         #  ('Kanye West', 'ahram.org.eg'),
#         #  ('Kanye West', 'lematin.ma'),
#         #  ('Kanye West', 'news24.com'),
#         #  ('Kanye West', 'premiumtimesng.com'),
#         #  ('Kanye West', 'nation.africa'),
#         #  ('Kanye West', 'graphic.com.gh'),
#         #  ('Donald Trump', 'thecitizen.co.tz'),
#         #  ('Kanye West', 'monitor.co.ug'),
#         #  ('Donald Trump', 'koreaherald.com'),
#         #  ('Kanye West', 'taipeitimes.com'),
#         #  ('Elon Musk', 'scmp.com'),
#         #  ('Kanye West', 'straitstimes.com'),
#         #  ('Elon Musk', 'thestar.com.my'),
#         #  ('Elon Musk', 'thejakartapost.com'),
#         #  ('Donald Trump', 'bangkokpost.com'),
#         #  ('Donald Trump', 'inquirer.net'),
#         #  ('Elon Musk', 'vnexpress.net'),
#         #  ('Donald Trump', 'dawn.com'),
#         #  ('Donald Trump', 'thedailystar.net')
#     ]

#     # [
#     #     ("Stefano Tomadini", "today.it"),
#     #     ("Stefano Tomadini", "libero.it"),
#     #     ("Stefano Tomadini", "zazoom.it"),
#     #     ("Matteo Garrone", "ansa.it"),
#     #     ("Matteo Garrone", "repubblica.it"),
#     #     ("Matteo Garrone", "corriere.it"),
#     #     ("Khaby Lame", "ilfattoquotidiano.it"),
#     #     ("Khaby Lame", "lastampa.it"),
#     #     ("Khaby Lame", "corriere.it"),
#     #     ("Kanye West", "ilfattoquotidiano.it"),
#     #     ("Kanye West", "lastampa.it"),
#     #     ("Kanye West", "corriere.it"),
#     #     ("Sam Altman", "ilfattoquotidiano.it"),
#     #     ("Sam Altman", "lastampa.it"),
#     #     ("Sam Altman", "corriere.it")
#     # ]

#     for name, domain in lista_test:
#         try:
#             demo(name, domain)
#         except Exception as e:
#             print(f"Errore durante l'esecuzione per {name} su {domain}: {e}")
