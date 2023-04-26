from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetchStats(selectedUser, df):
    extract = URLExtract()
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    numMessages = df.shape[0]
    word = []
    link = []
    for message in df['messages']:
        word.extend(message.split())
        link.extend(extract.find_urls(message))

    numWord = len(word)
    numMediaMsg = df[df['messages'] == '<Media omitted>\n'].shape[0]
    numLink = len(link)

    return numMessages, numWord, numMediaMsg, numLink


def fetchMostActive(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts().head()/df.shape[0])*100,
               2).reset_index().rename(columns={'index': 'name', 'user': 'percentage'})
    return x, df


def createWordCloud(selectedUser, df):

    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    f = open('hinglish.txt', 'r')
    stopWords = f.read()

    df = df[df['user'] != 'group_notification']
    df = df[df['messages'] != '<Media omitted>\n']

    def removStopWord(message):
        y = []
        for word in message.lower().split():
            if word not in stopWords:
                y.append(word)
        return " ".join(y)

    df['messages'] = df['messages'].apply(removStopWord)
    wc = WordCloud(width=500, height=500, min_font_size=18,
                   background_color='white')
    dfWc = wc.generate(df['messages'].str.cat(sep=" "))
    return dfWc


def mostUsedWord(selectedUser, df):

    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    f = open('hinglish.txt', 'r')
    stopWords = f.read()

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)

    temp = pd.DataFrame(Counter(words).most_common(20))
    return temp


def mostUsedEmoji(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df


def monthlyTimeline(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    timeline = df.groupby(['year', 'month_num', 'month']).count()[
        'messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def DailyTimeline(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    dailyTimeline = df.groupby('onlyDate').count()['messages'].reset_index()

    return dailyTimeline


def weekActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    return df['DayName'].value_counts()


def MonthActivityMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    return df['month'].value_counts()


def heatMap(selectedUser, df):
    if selectedUser != 'Overall':
        df = df[df['user'] == selectedUser]

    heatMAp = df.pivot_table(
        index="DayName", columns='period', values='messages', aggfunc='count').fillna(0)

    return heatMAp
