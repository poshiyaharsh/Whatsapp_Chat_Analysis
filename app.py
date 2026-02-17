import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

# Global visual style for better readability
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.figsize": (8, 4),
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    # Use emoji-capable font where available (Windows)
    "font.family": "Segoe UI Emoji",
})

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # optional date range filter
    min_date = df['only_date'].min()
    max_date = df['only_date'].max()
    date_range = st.sidebar.date_input(
        "Filter by date range (optional)",
        value=(min_date, max_date)
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['only_date'] >= start_date) & (df['only_date'] <= end_date)]

    # optional keyword filter
    keyword = st.sidebar.text_input("Filter messages containing (optional)")
    if keyword:
        df = df[df['message'].str.contains(keyword, case=False, na=False)]

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area (always on Overview tab)
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)

        overview_tab, timeline_tab, activity_tab, words_tab, advanced_tab = st.tabs(
            ["Overview", "Timelines", "Activity", "Words & Emojis", "Advanced"]
        )

        with overview_tab:
            st.title("Top Statistics")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

        with timeline_tab:
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots(figsize=(10,4))
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with activity_tab:
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots(figsize=(6,4))
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots(figsize=(6,4))
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots(figsize=(8,4))
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots(figsize=(8,4))

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            st.title("Hourly Activity")
            hourly_activity = helper.hourly_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(10,4))
            ax.bar(hourly_activity.index, hourly_activity.values, color="skyblue")
            ax.set_xlabel("Hour of day")
            ax.set_ylabel("Number of messages")
            st.pyplot(fig)

        with words_tab:
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots(figsize=(6,4))
            ax.imshow(df_wc)
            st.pyplot(fig)

            st.title('Most commmon words')
            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots(figsize=(8,4))
            ax.barh(most_common_df[0],most_common_df[1],color="teal")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user,df)

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df.head(20), width='stretch')
            with col2:
                fig,ax = plt.subplots(figsize=(6,6))
                ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%0.2f",
                    textprops={'fontname': 'Segoe UI Emoji'}
                )
                st.pyplot(fig)

        with advanced_tab:
            st.title("Sentiment Overview (English texts)")
            sentiments = helper.sentiment_overview(selected_user, df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Positive %", sentiments['positive'])
            col2.metric("Neutral %", sentiments['neutral'])
            col3.metric("Negative %", sentiments['negative'])

            st.title("Message Length Distribution")
            lengths, avg_words = helper.message_length_stats(selected_user, df)
            fig, ax = plt.subplots(figsize=(10,4))
            ax.hist(lengths, bins=20, color="slateblue")
            ax.set_xlabel("Words per message")
            ax.set_ylabel("Number of messages")
            st.pyplot(fig)
            st.metric("Average words per message", avg_words)

            st.title("User Comparison")
            comp_users = [u for u in user_list if u != "Overall"]
            if len(comp_users) >= 2:
                col1, col2 = st.columns(2)
                user_a = col1.selectbox("User A", comp_users, key="user_a")
                user_b = col2.selectbox("User B", comp_users, index=1 if len(comp_users) > 1 else 0, key="user_b")

                if user_a != user_b:
                    a_msgs, a_words, a_media, a_links = helper.fetch_stats(user_a, df)
                    b_msgs, b_words, b_media, b_links = helper.fetch_stats(user_b, df)

                    comp_col1, comp_col2 = st.columns(2)
                    with comp_col1:
                        st.subheader(user_a)
                        st.metric("Messages", a_msgs)
                        st.metric("Words", a_words)
                        st.metric("Media", a_media)
                        st.metric("Links", a_links)
                    with comp_col2:
                        st.subheader(user_b)
                        st.metric("Messages", b_msgs)
                        st.metric("Words", b_words)
                        st.metric("Media", b_media)
                        st.metric("Links", b_links)

            st.title("Export")
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download filtered chat data (CSV)",
                data=csv_data,
                file_name="whatsapp_chat_filtered.csv",
                mime="text/csv"
            )











