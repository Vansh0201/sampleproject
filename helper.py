from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
        
    
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return num_messages,len(words),len(links)

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=""))
    return df_wc
    
def most_common_words(selected_user, df):
    
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

        
    most_common_df = pd.DataFrame(Counter(words).most_common(10),
                                  columns=['Word', 'Count'])
    return most_common_df


    
