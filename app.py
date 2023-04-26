import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file", type='txt')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # fetch unique users
    userList = df['user'].unique().tolist()
    userList.remove('group_notification')
    userList.sort()
    userList.insert(0, "Overall")

    selectedUser = st.sidebar.selectbox("Show Analysis wrt", userList)

    if st.sidebar.button("Show Analysis"):
        numMessages, numWord, numMediaMsg, numLink = helper.fetchStats(
            selectedUser, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(numMessages)

        with col2:
            st.header("Total Words")
            st.title(numWord)

        with col3:
            st.header("Media Shared")
            st.title(numMediaMsg)

        with col4:
            st.header("Link Shared")
            st.title(numLink)

        # Time based analysis - Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthlyTimeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        dailyTimeline = helper.DailyTimeline(selectedUser, df)
        fig, ax = plt.subplots()
        ax.plot(dailyTimeline['onlyDate'],
                dailyTimeline['messages'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busyDay = helper.weekActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyDay.index, busyDay.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busyMonth = helper.MonthActivityMap(selectedUser, df)
            fig, ax = plt.subplots()
            ax.bar(busyMonth.index, busyMonth.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heat map
        st.title("Weekly Activity Map")
        UserHeatMap = helper.heatMap(selectedUser, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(UserHeatMap)
        st.pyplot(fig)

        # finding buisiest user in group
        if (selectedUser == 'Overall'):
            st.title('Most Active Users')
            x, newDf = helper.fetchMostActive(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(newDf)

        # wordcloud form
        st.title("Word Cloud")
        dfWC = helper.createWordCloud(selectedUser, df)
        fig, ax = plt.subplots()
        ax.imshow(dfWC)
        st.pyplot(fig)

        # Most used words
        st.title("Most used words")
        temp = helper.mostUsedWord(selectedUser, df)
        fig, ax = plt.subplots()
        ax.barh(temp[0], temp[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # MOST Used emoji

        st.title("Most Used Emoji")
        emojiDf = helper.mostUsedEmoji(selectedUser, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emojiDf)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emojiDf[1].head(), labels=emojiDf[0].head(), autopct="%.2f")
            st.pyplot(fig)
