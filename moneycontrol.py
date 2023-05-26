def moneycontrol(page=2):
    import pandas as pd
    import json
    import requests
    import sentiment
    import re
    from bs4 import BeautifulSoup
    from datetime import datetime, timedelta
    current_date = datetime.now().date()
    previous_date = current_date - timedelta(days=1)
    def article_info(url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        script_elements = soup.find_all("script", {"type": "application/ld+json"})
        script_text = script_elements[2].text.strip()
        script_text = script_text.replace('<script type="application/ld+json">', '').replace('</script>', '')
        script_text = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", script_text)
        data = json.loads(script_text)
        article_body = data[0].get("articleBody", "")
        return article_body
    def extract_date(date_string):
        date_string = date_string.replace(" IST", "")
        date_obj = datetime.strptime(date_string, "%B %d, %Y %I:%M %p")
        date_obj += timedelta(hours=5, minutes=30)
        formatted_date = date_obj.strftime("%d/%m/%Y")
        return formatted_date
    def extract_time(date_string):
        date_string = date_string.replace(" IST", "")
        date_obj = datetime.strptime(date_string, "%B %d, %Y %I:%M %p")
        formatted_time = date_obj.strftime("%I:%M %p")
        return formatted_time
    link=[]
    title=[]
    date=[]
    time=[]
    for i in range(1,page+1):
        url=f"https://www.moneycontrol.com/news/stocksinnews-142.html/page-{i}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        news_list=soup.find_all("li",{"class":"clearfix"})
        for news in news_list:
            link.append(news.find("a")['href'])
            title.append(news.find("a")['title'])
            date.append(extract_date(news.find("span").text))
            time.append(extract_time(news.find("span").text)) 
    data = pd.DataFrame({"Headline":title,"URL":link,"Date":date,"Time":time})
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    data['Normal Score'] = data['Headline'].apply(sentiment.analyze_sentiment)
    filtered_df = data.loc[(data['Date'] <= pd.to_datetime(current_date)) & (data['Date'] >= pd.to_datetime(previous_date))].reset_index(drop=True)
    dip=[]
    for url in filtered_df['URL']:
        if url is not None:
            dip.append(sentiment.predict_stock_sentiment(article_info(url)))
    filtered_df["Deep Score"] = dip
    return filtered_df
