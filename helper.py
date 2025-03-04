import pandas as pd
from collections import Counter
def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    
    #fetch no of messages   
    num_messages = df.shape[0]
    
    #fetch no of words
    words = []
    for message in df['message']:
        words.extend(message.split())
        
    #fetch no of media messages
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
    
    
    return num_messages,len(words),num_media_messages

def most_busy_users(df):
    x = df['user'].value_counts().head()
    # df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    df_percentage = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percentage.columns = ['name', 'percent']
    return x,df_percentage

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
             words.append(word)
             
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
    
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()
    
    
def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
   
        
# def activity_heatmap(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    # return user_heatmap
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Define the correct day and time order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    time_order = (
        ["12AM-1AM"] +
        [f"{hour}AM-{hour + 1}AM" for hour in range(1, 12)] +
        ["12PM-1PM"] +
        [f"{hour - 12}PM-{hour - 11}PM" for hour in range(13, 24)]
    )

    # Set day_name as a categorical variable with the correct order
    df['day_name'] = pd.Categorical(df['day_name'], categories=day_order, ordered=True)

    # Create the pivot table
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    # Reorder columns (time periods) and rows (days)
    user_heatmap = user_heatmap.reindex(columns=time_order, fill_value=0).reindex(day_order, fill_value=0)

    return user_heatmap
