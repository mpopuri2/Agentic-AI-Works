# class Data_Retrival:
#     def __init__(self, Query, max_results):
#         self.google_api_key = "AIzaSyBsLHUrqjx-z-FaAQtVp8erVhYIkNqYsGM"
#         self.custom_search_engine_ID = "4776c2f0b294a4715"
#         self.Query = Query
#         self.url = "https://www.googleapis.com/customsearch/v1"
#         self.max_results = max_results
#     def get_data(self):
#         self.parameters = {"key" : self.google_api_key, "cx" : self.custom_search_engine_ID, "q" : self.Query, "num" : self.max_results}
#         response = requests.get(self.url, params=self.parameters)
#         data = response.json()
#         print("Raw DATA -----> ",response.text)
#         print(response.json())
#         results = []
#         if "items" in data:
#             for item in data["items"]:
#                 results.append({"Title" : item.get("title"), "Link" : item.get("link"), "Snippet" : item.get("snippet")})
#         return results

# def fetch_medline(query, max_results=5):
#     url = "https://wsearch.nlm.nih.gov/ws/query"
#     params = {
#         "db": "healthTopics",
#         "term": query,
#         "retmax": max_results
#     }

#     resp = requests.get(url, params=params)
#     if resp.status_code != 200:
#         return []

#     texts = ""
#     for line in resp.text.split("<content name=\"FullSummary\">")[1:]:
#         summary = line.split("</content>")[0]
#         texts += "\n" + summary

#     return texts

    
# # print(fetch_medline("heart attacks?"))

import requests
from bs4 import BeautifulSoup

def fetch_medline(query, max_results=5):
    url = "https://connect.medlineplus.gov/service"

    params = {
        "mainSearchCriteria.v.c": query,
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.90",
        "knowledgeResponseType": "application/json",
        "informationRecipient.languageCode.c": "en"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = []

    entries = data.get("feed", {}).get("entry", [])
    for entry in entries[:max_results]:
        title = entry.get("title", {}).get("_value", "")
        summary = entry.get("summary", {}).get("_value", "")
        link = entry.get("link", [{}])[0].get("href", "")

        if summary:
            results.append({
                "title": title,
                "content": summary,
                "source": "MedlinePlus",
                "url": link
            })

    return results


def pubmed_search(query, max_results=5):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data["esearchresult"]["idlist"]

def pubmed_fetch(pmids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.text


def parse_pubmed(xml_data):
    soup = BeautifulSoup(xml_data, "xml")
    results = []

    articles = soup.find_all("PubmedArticle")
    for article in articles:
        title = article.find("ArticleTitle")
        abstract = article.find("AbstractText")
        pmid = article.find("PMID")

        if title and abstract:
            results.append({
                "title": title.text,
                "content": abstract.text,
                "source": "PubMed",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid.text}/"
            })

    return results


def fetch_medical_data(query):
    results = fetch_medline(query)
    print("-"*15 + "MEDLINE PLUS DATA" + "-"*15)
    print(results)


    print("*"*15 + "PUBMED DATA" + "*"*15)
    total_text = sum(len(r["content"]) for r in results)

    if total_text < 500:
        pmids = pubmed_search(query)
        if pmids:
            xml_data = pubmed_fetch(pmids)
            pubmed_results = parse_pubmed(xml_data)
            results.extend(pubmed_results)

    return results

print("~"*15 + "ABOUT HEART ATTACKS" + "~"*15)
print(fetch_medline("Heart attack"))

print("~"*15 + "ABOUT DIABETES" + "~"*15)
print(fetch_medline("Diabetes"))

print("~"*15 + "ABOUT HYPERTENSION" + "~"*15)
print(fetch_medline("Hypertension"))

print(fetch_medline("I21"))






