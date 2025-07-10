"DEMO STREAMLIT"

import json
from datetime import datetime
import streamlit as st
import requests


def is_valid_image_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and "image" in content_type
    except Exception:
        return False


st.set_page_config(page_title="Demo MASS", layout="wide")

col1, col2 = st.columns([0.3, 0.7])
with col1:
    st.image("https://www.codertd.com/wp-content/uploads/2023/09/Logo_code_RTD.png",
             width=200)  # Cambia URL se hai un logo
with col2:
    st.markdown("# MASS")
    st.markdown("##### Multi Agent Scraping Service")
    st.markdown("##### By CoDeRTD")
st.markdown("---")

uploaded_file = st.file_uploader("Carica file JSON", type="json")

if uploaded_file is not None:
    try:
        json_data = dict(json.load(uploaded_file))

        keyword = json_data.get("keyword", "")
        domain = json_data.get("domain", "")
        timestamp = json_data.get("timestamp", "")
        references = []
        if "references" in json_data.keys():
            references = json_data.get("references", [])
        elif "data" in json_data.keys():
            if "references" in json_data['data']:
                references = json_data['data'].get("references", [])
            elif "videos" in json_data['data']:
                references = json_data['data'].get("videos", [])
        elif "results" in json_data.keys():
            references = json_data.get("results", [])

        try:
            dt_obj = datetime.fromisoformat(timestamp)
            timestamp_it = dt_obj.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            timestamp_it = "Formato non valido"

        # Visualizza parametri ricerca
        with st.container():
            st.markdown("### 📌 Parametri della ricerca")
            col1, col2, col3 = st.columns(3)
            col1.metric("🔍 Keyword", keyword)
            col2.metric("🌐 Dominio", domain)
            col3.metric("🕒 Timestamp", timestamp_it)

        st.markdown("---")
        st.markdown(f"### 🎬 Risultati trovati: {len(references)}")

        # Tabella moderna
        index = 0
        for ref in references:
            index += 1
            with st.container():
                index_col, thumb_col, info_col, link_col = st.columns(
                    [0.1, 0.2, 0.6, 0.1])
                with index_col:
                    st.markdown(f"{index}")

                with thumb_col:
                    thumbnail_url = ref.get("thumbnail_url", "")
                    if thumbnail_url and is_valid_image_url(thumbnail_url):
                        st.image(thumbnail_url, width=120)
                    else:
                        # Mostra un'immagine placeholder
                        st.image(
                            "https://via.placeholder.com/120x90?text=N/A", width=120)

                with info_col:
                    st.markdown(f"**{ref.get('title', 'Senza titolo')}**")
                    st.markdown(f"{ref.get('content', '')}")

                with link_col:
                    url = ref.get("url", "#")
                    st.markdown(f"[🔗 Link]({url})", unsafe_allow_html=True)

                st.markdown("---")

    except Exception as e:
        st.error("Errore durante la lettura del file JSON.")
        st.exception(e)
