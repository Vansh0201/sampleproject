import re
import pandas as pd

def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s[^\]]+\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [d.strip('[]').strip() for d in dates]
    dates = [d.replace('[', '').replace(']', '').replace('\u202f', ' ').replace('\xa0', ' ').strip()
             for d in dates]
    df = pd.DataFrame({'user_message': messages, 'date': dates})

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p')

    users = []
    messages = []
    for m in df['user_message']:
        match = re.match(r'([^:]+):\s(.*)', m)  # split at first ": "
        if match:
            users.append(match.group(1).strip())     # username only
            messages.append(match.group(2).strip())  # message only
        else:
            users.append('group_notification')       # system/group messages
            messages.append(m.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    df['year']=df['date'].dt.year

    df['month']=df['date'].dt.month_name()

    df['day'] =df['date'].dt.day

    df['hour']=df['date'].dt.hour

    df['minute']=df['date'].dt.minute
    
    return df;

