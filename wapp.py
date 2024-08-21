import streamlit as st
import pandas as pd
from preprocessor import preprocess  # Import the preprocess function from preprocessor.py
from helper import fetch_stats
# Streamlit app code
st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat_data = bytes_data.decode("utf-8").splitlines()  # Convert bytes to string and split into lines

    try:
        df = preprocess(chat_data)  # Pass the list of lines to preprocess
        if isinstance(df, pd.DataFrame):
            st.dataframe(df)  # Display DataFrame in Streamlit
        else:
            st.error("The preprocess function did not return a DataFrame.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
    
    # fetch uniquie sender
    #df['Sender'] = df['Sender'].astype(str)
    sender_list = df['Sender'].unique().tolist()
    sender_list.sort()
    sender_list.insert(0,"Overall")
    selected_sender = st.sidebar.selectbox('show analsis wrt', sender_list)
    
    if st.sidebar.button('Show analsis'):
        
        num_messages, words, number_media_messages = fetch_stats(selected_sender,df)
        
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header('Total media_messages')
            st.title(number_media_messages)