import streamlit as st
from preprocessor import preprocess

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file", type="txt")
if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    string_data = bytes_data.decode("utf-8")
    df = preprocess(string_data)
    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        st.bar_chart(df['message'].value_counts())


