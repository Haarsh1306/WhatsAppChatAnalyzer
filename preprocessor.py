import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    pattern1 = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    cnt = 0
    if len(re.split(pattern1, data)[1:]) == 0:
        messages = re.split(pattern, data)[1:]
        cnt = 0
    else:
        messages = re.split(pattern1, data)[1:]
        cnt = 1

    if len(re.findall(pattern1, data)) == 0:
        dates = re.findall(pattern, data)
    else:
        dates = re.findall(pattern1, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    if cnt == 0:
        format = '%m/%d/%y, %I:%M %p - '
    else:
        format = '%d/%m/%y, %H:%M - '

    df['message_date'] = pd.to_datetime(
        df['message_date'], format=format)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    user = []
    message = []
    for messages in df['user_message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group_notification')
            message.append(entry[0])
    df['user'] = user
    df['messages'] = message
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['onlyDate'] = df['date'].dt.date
    df['DayName'] = df['date'].dt.day_name()

    period = []
    for hour in df[['DayName', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df
