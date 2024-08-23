from urlextract import URLExtract
urlextract = URLExtract()
def fetch_stats(selected_sender, df):
    if selected_sender != 'Overall':
        df = df[df['Sender']==selected_sender]
        
    num_messages = df.shape[0]
    words = []
    for word in df['Message']:
        words.extend(word.split())
        
    number_media_messages = df[df['Message']== '<Media omitted>'].shape[0]
    links = []
    for url in df.Message:
        links.extend(urlextract.find_urls(url))
    return num_messages, len(words), number_media_messages, len(links)
    