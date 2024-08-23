from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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
    if selected_sender != 'Overall':
        df = df[df['Sender'] == selected_sender]
    wc = WordCloud(width=500,height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=' '))
    return df_wc