"""Google API Search module."""
from googleapiclient.discovery import build
from config import Config


class GoogleAPI():
    def __init__(self):
        self.my_api_key = Config.env.get("G_API_KEY")
        self.my_cse_id = Config.env.get("G_CSE_ID")
        self.service = build("customsearch", "v1",
                             developerKey=self.my_api_key)

    def search(self, query: str, **kwargs) -> list:
        res = dict(self.service.cse().list(
            q=query, cx=self.my_cse_id, sort="date", **kwargs).execute())
        elements = []
        if res.get('items'):
            for el in res.get('items'):
                el = dict(el)
                if not el.get('pagemap'):
                    el['pagemap'] = {
                        'cse_thumbnail': ''
                    }
                elements.append({
                    'title': el['title'],
                    'url': el['link'],
                    'description': el['snippet'],
                    'domain': el['displayLink'],
                    "thumbnail": el['pagemap'].get('cse_thumbnail')[0]['src'] if el['pagemap'].get('cse_thumbnail') else None
                })
        return elements

    def searchImage(self, query: str, **kwargs) -> list:
        res = dict(self.service.cse().list(
            q=query, cx=self.my_cse_id, searchType='image', sort="date", **kwargs).execute())
        elements = []
        if res.get('items'):
            for el in res.get('items'):
                el = dict(el)
                elements.append({
                    "title": el.get('title'),
                    "url": el.get('image')['contextLink'],
                    "description": el.get('snippet'),
                    "domain": el['displayLink'],
                    "thumbnail": el.get('link'),
                })
        return elements


def search_query(name: str, domain: str, **kwargs) -> list:
    google_api = GoogleAPI()
    elements = google_api.search(query=f'"{name}"', siteSearch=domain) or []
    for i in range(1, 10):
        try:
            res = google_api.search(
                query=f'"{name}"', siteSearch=domain, start=i*10+1)
            elements = elements+res
        except:
            return elements
    return elements


def search_image_query(name: str, domain: str, **kwargs) -> list:
    google_api = GoogleAPI()
    elements = google_api.searchImage(
        query=f'"{name}"', siteSearch=domain) or []
    for i in range(1, 10):
        try:
            res = google_api.searchImage(
                query=f'"{name}"', siteSearch=domain, start=i*10+1)
            elements = elements+res
        except:
            return elements
    return elements


if __name__ == "__main__":
    print(search_image_query("khaby lame", "lastampa.it"))
    print(search_query("khaby lame", "lastampa.it"))
