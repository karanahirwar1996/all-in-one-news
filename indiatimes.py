def india_times(page_count=4):
    import sentiment
    import pandas as pd 
    import json
    import requests
    import nltk
    from bs4 import BeautifulSoup
    from datetime import datetime, timedelta
    def extract_date(date_string):
        date_string = date_string.replace(" IST", "")
        datetime_obj = datetime.strptime(date_string, "%B %d, %Y, %I:%M %p")
        formatted_date = datetime_obj.strftime("%d/%m/%Y")
        return formatted_date
    def extract_time(date_string):
        date_string = date_string.replace(" IST", "")
        datetime_obj = datetime.strptime(date_string, "%B %d, %Y, %I:%M %p")
        formatted_date = datetime_obj.strftime("%I:%M %p")
        return formatted_date
    current_date = datetime.now().date()
    previous_date = current_date - timedelta(days=1)

    url = 'https://economictimes.indiatimes.com/markets/stocks/earnings/news'
    base_url = 'https://economictimes.indiatimes.com'
    tag = []
    href = []
    date=[]
    time=[]
    page = 1

    while page <= page_count:
        res = requests.get(url, params={'page': page})
        soup = BeautifulSoup(res.content, features="html.parser")
        if not soup.find_all("div", {"class": "eachStory"}):
            break
        for items in soup.find_all("div", {"class": "eachStory"}):
            tag.append(items.find("a").text)
            href.append(base_url + items.find('a')['href'])
            date.append(extract_date(items.find('time',{"class":"date-format"}).text))
            time.append(extract_time(items.find('time',{"class":"date-format"}).text))
        page += 1
    data = pd.DataFrame({'Headline': tag, 'URL': href,"date":date,"Time":time})
    data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')
    filtered_df = data.loc[(data['date'] <= pd.to_datetime(current_date)) & (data['date'] >= pd.to_datetime(previous_date))]
    dip=[]
    for u in list(filtered_df["URL"]):
        res = requests.get(u)
        dip_soup = BeautifulSoup(res.content, features="html.parser")
        script_tag=dip_soup.find_all("script",{"type":"application/ld+json"})[1]
        script_data = script_tag.string.strip()
        data = json.loads(script_data)
        article_body = data.get("articleBody")
        dip.append(sentiment.predict_stock_sentiment(article_body) if article_body else None)
    filtered_df["Deep Score"]=dip
    filtered_df['Normal Score']=filtered_df['Headline'].apply(sentiment.analyze_sentiment)
    return filtered_df
