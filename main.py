import indiatimes
import business
import posemails
import pandas as pd
df1=indiatimes.india_times()
df2=business.positive_news()
concat_df=pd.concat([df1,df2],ignore_index=True)
sorted_df=concat_df.loc[(concat_df['Deep Score']>45)&(concat_df['Normal Score']>0)]
posemails.pos_email(sorted_df,concat_df)
