from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

urlextract = URLExtract()

def fetch_stats(selected_sender, df):
    if selected_sender != 'Overall':
        df = df[df['Sender'] == selected_sender]
        
    num_messages = df.shape[0]
    words = df['Message'].str.split().str.len().sum()  # Efficient word counting
    number_media_messages = df[df['Message'] == '<Media omitted>'].shape[0]
    links = sum(df['Message'].apply(lambda x: len(urlextract.find_urls(x))))
    
    return num_messages, words, number_media_messages, links


def most_busy_users(df):
    x = df.Sender.value_counts().head(5)
    new_df = round((df.Sender.value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'Sender':'name','count':'percent'})   
    return x, new_df

def create_wordcloud(selected_sender, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_sender != 'Overall':
        df = df[df['Sender'] == selected_sender]
    temp  = df[df['Message'] != '<Media omitted>']  
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return' '.join(y)
            
    
    wc = WordCloud(width=500,height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=' '))
    return df_wc
def most_common_words(selected_sender, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_sender != 'Overall':
        df = df[df['Sender'] == selected_sender]
    temp  = df[df['Message'] != '<Media omitted>']
    words = []
    for message in temp.Message:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    m_c_df = pd.DataFrame(Counter(words).most_common(20))
    return m_c_df

def emoji_helper(selected_sender, df):
    if selected_sender != 'Overall':
        df = df[df['Sender'] == selected_sender]
    emojis = []
    for message in df.Message:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df
    
    
        
    