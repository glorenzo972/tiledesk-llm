
from langchain_community.document_loaders import BSHTMLLoader

from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import AsyncChromiumLoader
import requests
import logging

logger = logging.getLogger(__name__)


# "https://help.tiledesk.com/mychatbots/articles/il-pnrr-per-la-ricerca-e-linnovazione/"
def get_content_by_url(url: str, scrape_type: int):
    try:
        urls = [url]
        if scrape_type == 0:
            loader = UnstructuredURLLoader(
                urls=urls, mode="elements", strategy="fast", continue_on_failure=False
            )
        else:
            loader = UnstructuredURLLoader(
                urls=urls, mode="single", continue_on_failure=False
            )
        docs = loader.load()

        # from pprint import pprint
        # pprint(docs)

        return docs
    except Exception as ex:
        raise ex


def load_document(url: str, type_source: str):
    # import os
    # name, extension = os.path.splitext(file)

    if type_source == 'pdf':
        from langchain_community.document_loaders import PyPDFLoader
        logger.info(f'Loading {url}')
        loader = PyPDFLoader(url)
    elif type_source == 'docx':
        from langchain_community.document_loaders import Docx2txtLoader
        logger.info(f'Loading {url}')
        loader = Docx2txtLoader(url)
    elif type_source == 'txt':
        from langchain_community.document_loaders import TextLoader
        logger.info(f'Loading {url}')
        loader = TextLoader(url)
    else:
        logger.info('Document format is not supported!')
        return None

    data = loader.load()
    return data


def load_from_wikipedia(query, lang='en', load_max_docs=2):
    from langchain_community.document_loaders import WikipediaLoader
    loader = WikipediaLoader(query=query, lang=lang, load_max_docs=load_max_docs)
    data = loader.load()
    return data


def get_content_by_url_with_bs(url:str):
    html = requests.get(url)
    # urls = [url]
    # Load HTML
    # loader = await AsyncChromiumLoader(urls)
    # html = loader.load()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html.content, 'html.parser')

    # Estrai tutte le sezioni h1
    h1_tags = soup.find_all('h1')

    testi = []
    for index, h1_tag in enumerate(h1_tags):
        # Trova il tag <table> successivo al tag <h1>
        next_a = h1_tag.find_next_sibling('a')
        next_desc = h1_tag.find_next_sibling('h2')


        next_table = h1_tag.find_next_sibling('table')

        # Se esiste, estrai le righe (tr) all'interno della tabella
        testo_tabella =""
        if next_table:
            rows = next_table.find_all('tr')
            # Stampa il contenuto delle righe
            for row in rows:
                # Estrai i td
                tds = row.find_all('td')
                # Se ci sono almeno due td
                if len(tds) >= 2:
                    # Stampa il testo del primo td, i due punti e il testo del secondo td
                    testo_tabella+=f"  {tds[0].get_text(strip=True)}: {tds[1].get_text(strip=True)}"

        testo_doc = f"Product: {h1_tag.text}, URL: {next_a['href']} description: {next_desc.text}.  Measurements: {testo_tabella}"
        testi.append(testo_doc)

        # Aggiungi una riga vuota tra i segmenti
        # if index < len(h1_tags) - 1:
        #    print()  # Stampa una riga vuota tra i segmenti


    return testi



