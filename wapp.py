import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from preprocessor import preprocess  # Import the preprocess function from preprocessor.py
from helper import fetch_stats, most_busy_users, create_wordcloud, most_common_words, emoji_helper, monthly_timeline

# Streamlit app code
st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat_data = bytes_data.decode("utf-8").splitlines()  # Convert bytes to string and split into lines

    try:
        df = preprocess(chat_data)  # Pass the list of lines to preprocess
        if isinstance(df, pd.DataFrame):
            #st.dataframe(df)  # Display DataFrame in Streamlit
            pass
        else:
            st.error("The preprocess function did not return a DataFrame.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
    # fetch unique senders
    sender_list = df['Sender'].unique().tolist()
    sender_list.sort()
    sender_list.insert(0, "Overall")
    selected_sender = st.sidebar.selectbox('Show analysis for', sender_list)
    
    if st.sidebar.button('Show analysis'):
        
        num_messages, words, number_media_messages, links = fetch_stats(selected_sender, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header('Total Media Messages')
            st.title(number_media_messages)
        with col4:
            st.header('Total Links')
            st.title(links)
            
        # timeline
        st.title('Monthly Timeline')
        timeline = monthly_timeline(selected_sender, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['Message'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Finding the busiest user in the group
        if selected_sender == 'Overall':
            st.title('Most Busy Users')
            x, new_df = most_busy_users(df)
            
            fig, ax = plt.subplots()  # Create figure and axes
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values, color='red')  # Create bar chart
                plt.xticks(rotation='vertical')
                st.pyplot(fig)  # Display the plot
            with col2:
                st.dataframe(new_df)  # Display DataFrame of busiest users
                
        # wordcloud
        st.title('Wordcloud') 
        df_wc = create_wordcloud(selected_sender, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)  
        
        #most_common_words
        st.title('Most Common Words')
        m_c_df = most_common_words(selected_sender, df)
        fig, ax = plt.subplots()
        ax.barh(m_c_df[0], m_c_df[1])
        #plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #st.dataframe(m_c_df)
        
        # Emoji analysis
        st.title('emoji analysis')
        emoji_df = emoji_helper(selected_sender, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)