"""Firecrawl Search Example"""
# Install with pip install firecrawl-py
import json
from firecrawl import FirecrawlApp, ScrapeOptions, JsonConfig
from pydantic import BaseModel
from datetime import datetime


STAMPA = "https://lastampa.it/ricerca?query="
CORRIERE = "https://www.corriere.it/ricerca/?q="
FATTO = "https://www.ilfattoquotidiano.it/?s="
REP = "https://www.repubblica.it/ricerca/?query="
POST = "https://www.ilpost.it/cerca/?qs="
SECOLO = "https://www.secoloditalia.it/ricerca/?q="
OGGI = "https://www.oggi.it/ricerca/?q="


def main(fullname: str, domain: str, search_url: str) -> list:
    # Use the synchronous FirecrawlApp instead of AsyncFirecrawlApp
    app = FirecrawlApp(api_key='fc-1229aa3cfb6f4b969eb51b15e2768f0c')

    class ExtractSchema():
        title: str
        url: str

    json_config = JsonConfig(
        schema=ExtractSchema
    )
    all_pages = []
    for page in [1, 2]:
        print(f"******* start Page {page}*************")
        keywords_ext = fullname
        keywords = keywords_ext.split(" ")
        keywords = '+'.join(keywords)
        search_link = f'{search_url}{keywords}' + f"&page={page}"
        if page == 1:
            search_link = f'{search_url}{keywords}'
        map_result = app.extract(
            [search_link],
            prompt="""Extract all article-related information from each <div> that contains at least one <a> tag with an href attribute. For each article, return the following:

- "url": the href value from the <a> tag
- "title": if available, use the "title" attribute of the <a> tag; otherwise, use the visible text between <a>...</a>
- "thumbnail": if available, extract the "src" or "data-src" attribute from an <img> tag within the same <div>

Ignore any <div> elements used for navigation, footer, sidebar, ads, or promotional content (e.g., those with class names like "nav", "footer", "sidebar", "ads", "promo", etc.).

Return the output as a JSON.""",
            # timeout=120000,
            # formats=["json"],
            # json_options=json_config,
            # scrape_options=ScrapeOptions(formats=['links'])
        )
        print(map_result)
        print(f"******* end Page {page}*************")
        map_result = dict(map_result)
        all_pages = all_pages+list(map_result['data']['articles'])

    # Execute search with content scraping
    # response = app.search(
    #     query='khaby lame',
    #     limit=20,
    #     location='Italy',
    #     scrape_options=ScrapeOptions(formats=['links'])
    # )

    # Print the response

    # Optional: Save to a JSON file for easier viewing
    # Convert pydantic object to dict using model_dump for pydantic v2 or dict() for older versions
    # try:
    #     # Try pydantic v2 method first
    #     response_dict = response.model_dump()
    # except AttributeError:
    #     # Fall back to pydantic v1 method
    #     response_dict = response.dict()
    # except Exception:
    #     # Last resort: use __dict__ but this might not catch all nested objects
    #     response_dict = vars(response)
    domain = domain.split(".")[0] if "." in domain else domain
    filename = f'{"_".join(keywords_ext.split(" "))}_search_{domain}.json'
    schema = {
        "keyword": keywords_ext,
        "domain": domain,
        "timestamp": datetime.now(),
        "search_link": search_link,
        "unique_results": all_pages
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False,
                  indent=2, default=str)
    print(f"Results also saved to: {filename}")
    return schema["unique_results"]


if __name__ == "__main__":
    main("khaby lame", "corriere.it", CORRIERE)
# https://www.pornslash.com/search/martina+finocchio
