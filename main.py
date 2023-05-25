import indiatimes
import business
import posemails
import pandas as pd
import negemails
import shorturl
df1=indiatimes.india_times()
df2=business.positive_news()
df1["Source"]="EconomicTimes"
df2["Source"]="Business-standard"
concat_df=pd.concat([df1,df2],ignore_index=True)
concat_df["URL"]=concat_df["URL"].apply(shorturl.short_link)
sorted_df=concat_df.loc[(concat_df['Deep Score']>50)&(concat_df['Normal Score']>0)]
neg_df=concat_df.loc[(concat_df['Deep Score']<=0)&(concat_df['Normal Score']<=0)]
posemails.pos_email(sorted_df,concat_df)
negemails.neg_email(neg_df,concat_df)
