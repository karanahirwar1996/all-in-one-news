import sentiment
import pandas as pd
import json
import requests
import re
import nltk
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from multiprocessing import Pool

def extract_date(timestamp):
    date_str = timestamp.split("T")[0]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d/%m/%Y")
    return formatted_date

def extract_time(timestamp):
    time_str = timestamp.split("T")[1].split("+")[0]
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    formatted_time = time_obj.strftime("%I:%M %p")
    return formatted_time

def scrape_datetime(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, features="html.parser")
        script_elements = soup.find_all("script", {"type": "application/ld+json"})
        for script in script_elements:
            script_data = json.loads(script.string)
            if script_data.get("@type") == "NewsArticle":
                datetime = script_data.get("datePublished")
                return datetime
        return None
    except:
        return None

def scrape_article_info(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, features="html.parser")
        script_elements = soup.find_all("script", {"type": "application/ld+json"})
        for script in script_elements:
            script_data = json.loads(script.string)
            if script_data.get("@type") == "NewsArticle":
                article_body = script_data.get("articleBody")
                return article_body
        return None
    except:
        return None

def scrape_page(page_num):
    url = f'https://www.business-standard.com/amp/markets-news/page-{page_num}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features="html.parser")
    script_elements = soup.find_all("script", {"type": "application/ld+json"})
    if len(script_elements)!=5:
        return None
    json_data = json.loads(script_elements[4].string)
    data = [(item["name"], item["url"]) for item in json_data["itemListElement"]]
    return pd.DataFrame(data, columns=["Headline", "URL"])
def positive_news():
    current_date = datetime.now().date()
    previous_date = current_date - timedelta(days=1)

    dfs = []
    pool = Pool(processes=4)  # Adjust the number of processes based on your system
    results = pool.map(scrape_page, range(1,4))
    dfs = [df for df in results if df is not None]

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df = df.drop_duplicates(ignore_index=True)
    print(df.shape)

    results = pool.map(scrape_datetime, df['URL'])
    for i, result in enumerate(results):
        if result is not None:
            try:
                df.loc[i, 'Date'] = extract_date(result)
            except (KeyError, TypeError):
                df.loc[i, 'Date'] = None
            try:
                df.loc[i, 'Time'] = extract_time(result)
            except (KeyError, TypeError):
                df.loc[i, 'Time'] = None
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Normal Score'] = df['Headline'].apply(sentiment.analyze_sentiment)

    filtered_df = df.loc[(df['Date'] <= pd.to_datetime(current_date)) & (df['Date'] >= pd.to_datetime(previous_date))].reset_index(drop=True)

    dip = []
    results = pool.map(scrape_article_info, filtered_df['URL'])
    for result in results:
        if result is not None:
            dip.append(sentiment.predict_stock_sentiment(result))

    filtered_df["Deep Score"] = dip

    return filtered_df
