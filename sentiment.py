import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
nltk.download('punkt')
nltk.download('wordnet')
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
json={
  "type": "service_account",
  "project_id": "original-advice-385307",
  "private_key_id": "e221975bf7db75e9edcf752f7e6a5f1046979bff",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdETxBnUFb4obB\n/hE+cbda20oeN30WGdhnIfOdgaC2t/TfiDZTfcB856VOOAPixd4wIrjJUVWym6SZ\nksEGZt6vKPdoZ3X6SaavgOx1EjWl84YyJVyMAw623d5D8FWgzk1/10mnfCMhDqaw\ncDAh+Rm8TDZ9d0S69PB1KGNupz3hafKlxCpSQzCNfOYw6fO2wv+g3YWopLv1x6GR\nmVX5811GyM+lZOT8MaUmTloISBoO3O2GDJUPGXwZDvx9ymwPZ9bTHDTUP0iulrgG\nBjoa9lGWHPK2tYbEdnCdz99OOIBrMJcR36veeJISO3tC+gyAcmLstAfC4c5V6zD/\nsyHBJpY/AgMBAAECggEACidXv94h9YYFXtEaiEY4VjVK61J8UaDGGT9b964Dl7b4\nq41WBbu2uocMbAFkWZVKXHjs0obhhV8DxbHJAgLwbl5gRW2QIOgApePYZWZnSsfI\nFcHN48yRd5zhhil+lPCr7eca/yrKkpPXOXIR39Wx+4w/EYlToMpo07S9XiU4SN7D\nPvs0/QuSOt0PgyS9b9VcAV9Llzar/Zprye4S4HZfHh6Py5ikhEyjMNuIvOk5Elta\nHVY4HvP+nqmDD9E+5ea0BuphOdzTTwBo41ApWarZ8pL4OQVrse7d97dRHP30/5tn\nQjNXb35bGX+XTTx2i2jQkw/yj1cuiVCW3LK9WAbVgQKBgQDM3+egXkDKcsQTDKw5\nSwcTp9H5+sjsyMqi4oAVbuOQQgy1FiMswM92C0LWoGVvuR38HO007ZwrKz5DK6dX\nRm8W29gJwvgfZNjGc1tRCSGuXz6lhgaNOTY22KG8e9OaLlweUJ/ttztWwvCumccm\nsrXLC313knZZuS1XXLH+rDkk3wKBgQDEQzxf4dkcrpq14jOfUNt5KWMQLiUXoPBX\npgDAXqy6vZLb3oxG8Fi/jTRDnEvYkLHnLWcSeXYM+MOwVoJjbeAFMg4jzUbZS8Xt\nKJQmjV38hEcSA7+6yAtrmwwBnBu0je+mnwMjdJh6R//dVBg0AEpkKdpBwqncl/Xf\nmfb7rcBaoQKBgCuMsOTzBBzEto9CE13+Z9uywby8pXdH22MyeH2V28OvdpoLwaBi\nv/bcv/F1mPpdxFTyJS4qEBdREuQeZGz16OlYBB1XF30856OPo+qe4Uz6rAttaPke\nHzsbY434WGuezTAYfVZ/q5pux9ClmaLNPD2UDLCdLpE1/sBiUOfM3jzLAoGBAMNr\nz2oJkA2nLhV9Lrmr4V07gJBT4ksszSP4/zaNDqDCssCLUFIyb6wMBcZsknkJWps9\n8ivLFWjFKtUizqICfdWuibXMaIdlk6cZiKr6iGMvszSU1ww8tGJo+AOCVXPrAH2A\nR7e+GTVpC7RuT8s3ntstcU2Zb1lfVktXGz5vO+EBAoGBAJUx1cWDaO2+Dmjm5rd9\nM8wgDlsLVsswOP/SindXyFO1/s+tyrjp9INVe6Y2HBFMkhwsuO7jcfa35xIRN/j8\nSN+aciV0EjdruVtqfyPBnjbWA/KEBRz0UX3lpieJQDifkX4ezcklpqYoW32CMDF7\nHKLBuTaGfguAB62mW3UviM1R\n-----END PRIVATE KEY-----\n",
  "client_email": "gsapi300423@original-advice-385307.iam.gserviceaccount.com",
  "client_id": "100557238653230760997",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsapi300423%40original-advice-385307.iam.gserviceaccount.com"
}
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json, scope)
client = gspread.authorize(creds)
gs = client.open('Data_Source')
sheet_pos=gs.worksheet('Positive_Words')
sheet_neg=gs.worksheet('Negative_Words')
all_record_pos=sheet_pos.get_all_records()
pos_df=pd.DataFrame(all_record_pos)
all_record_neg=sheet_neg.get_all_records()
neg_df=pd.DataFrame(all_record_neg)
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    return sentiment_scores['compound'] * 100
def calculate_positivity_score(positive_count, negative_count):
    total_count = positive_count + negative_count
    positivity_score = (positive_count - negative_count) / total_count * 100 if total_count != 0 else 0
    return round(positivity_score, 2)

def predict_stock_sentiment(sentence):
    words = word_tokenize(sentence.lower())
    
    positive_keywords =list(pos_df['words'])
    negative_keywords =list(neg_df['words'])
    positive_count = 0
    negative_count = 0
    lemmatizer = WordNetLemmatizer()

    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        if lemma in positive_keywords:
            positive_count += 1

    for phrase in negative_keywords:
        if phrase in sentence:
            negative_count += 1

    positivity_score = calculate_positivity_score(positive_count, negative_count)

    return positivity_score
