import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import time
import json
from BE.config import Config


def extract_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Rimuove script, style, noscript
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return None


def analyze_sentiment_simple(subject_name, text):
    client = OpenAI(api_key=Config.env.get("OPENAI_API_KEY"))
    prompt = f"""You are a sentiment analysis tool.

    Analyze the sentiment of this article and respond in the following JSON format:

    {{
    "sentiment": "Positive | Negative | Neutral",
    "short_phrase": "A brief, impactful sentence (max 100 characters) that summarizes the article and gives a sense of why this sentiment was chosen.",
    "summary_reason": "A concise summary and justification for the sentiment (max 200 characters)."
    }}

    Important: The sentiment must be evaluated relative to {subject_name}, even if the overall article sentiment is different.

    Article text: {text} """

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis tool."},
                {"role": "user", "content": prompt}
            ]
        )
        sentiment = response.choices[0].message.content.strip()
        result = json.loads(sentiment)
        return dict(result)
    except Exception as e:
        return e


def analysis(name, urls):
    final_results = []
    for url in urls:
        text = extract_text(url)
        try:
            sentiment = analyze_sentiment_simple(name, text)
        except Exception as e:
            sentiment = str(e)
        final_results.append(
            {"url": url, "sentiment": sentiment['sentiment'], "summary": sentiment['summary_reason'], "phrase": sentiment['short_phrase']})
        time.sleep(1)

    return final_results


if __name__ == "__main__":
    URLS = [
        "https://www.lastampa.it/archivio/2021/05/19/news/khaby_il_torinese_che_batte_zuckerberg-30753/"
    ]
    results = analysis("khaby lame", URLS)
    for result in results:
        print(f"URL: {result['url']}, Sentiment: {result['sentiment']}")
