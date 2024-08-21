import streamlit as st
import pandas as pd
from preprocessor import preprocess  # Import the preprocess function from preprocessor.py

# Streamlit app code
st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat_data = bytes_data.decode("utf-8").splitlines()  # Convert bytes to string and split into lines
    
    #st.text("\n".join(chat_data))  # Display raw text for debugging
    
    try:
        df = preprocess(chat_data)  # Pass the list of lines to preprocess
        if isinstance(df, pd.DataFrame):
            st.dataframe(df)  # Display DataFrame in Streamlit
        else:
            st.error("The preprocess function did not return a DataFrame.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
