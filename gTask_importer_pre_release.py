#!/usr/bin/env python
# coding: utf-8

# ### Get Tasklists from Quickstart

# In[12]:


from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from tqdm import tqdm
import time

def google_authentication():
# If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']

    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    # if credential != None:
    #     creds = credential
    # else:
    #     creds = None
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    return service

def get_tasklists(service):
    
    # Call the Tasks API
    results = service.tasklists().list().execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        print('Task lists found')
        return items


# ### Get Tasks from Tasklists

GLOBAL_COUNTER = 0
# (tasklist=*, showCompleted=None, dueMin=None, dueMax=None, pageToken=None, updatedMin=None, showDeleted=None, completedMax=None, maxResults=None, completedMin=None, showHidden=None)
def get_tasks_from_tasklist(task_list_id, task_list_title, service):
    df = pd.DataFrame()
    next_page_token = None
    global GLOBAL_COUNTER

    while (True):
        task_results = service.tasks().list(tasklist=task_list_id, pageToken=next_page_token).execute()
        df = df.append(pd.DataFrame.from_dict(task_results['items']), sort=False)
        df['category'] = task_list_title
        GLOBAL_COUNTER = GLOBAL_COUNTER + len(task_results['items'])
        try:
            next_page_token = task_results['nextPageToken']
        except:
            return df


# ### Modify dataframe form

# In[125]:


def preprocess_df(df):
    df1 = df.rename(columns={'id': 'parent','title': 'parent_title'})
    df2 = df[['id', 'title']].rename(columns={'id': 'parent','title': 'parent_title'})
    df3 = df1.merge(df2, on='parent', how ='left')
    df3 = df3.sort_values(by='parent_title')
    return df3[['category','parent_title', 'title', 'notes', 'updated', 'selfLink']]

def get_csv_from_tasks():
    service = google_authentication()

    ### Initialize Dataframe
    df_result = pd.DataFrame()

    ### Get Tasklists from Quickstart
    items = get_tasklists(service)
    for item in tqdm(items):
        ### Get Tasks from Tasklists
        # function call
        df_result = df_result.append(get_tasks_from_tasklist(item['id'], item['title'], service), sort=False)

    ### Modify dataframe form
    df_result = preprocess_df(df_result)
    df_result.to_csv('gTasks.csv', sep='\t', encoding='utf-8')
    return len(df_result)==GLOBAL_COUNTER

# ### Combine functions to make CSV file 
def main():
# In[135]:
    get_csv_from_tasks()
    
if __name__ == '__main__':
    main()


