import requests
import json
import csv
import pandas as pd
import io
import numpy as np


def get_object(url):
    #url = f"https://jsonplaceholder.typicode.com/todos"
    r = requests.get(url)
    json_object = json.loads(r.text)
    #print(json_object)
    #print("-----------")
    #print(len(json_object))
    #print(type(json_object))
    return json_object


def json_to_dataframe(url):
    o_json = get_object(url)
    dataframe = pd.DataFrame(o_json)
    blankIndex=[''] * len(dataframe)
    dataframe.index=blankIndex
    #print(dataframe)
    return dataframe

def completed_task():
    """ give the task completed by joiner"""
    data = json_to_dataframe( url = f"http://service3-django:8010/task/")
    clean_data = data[["joiner_id", "completed"]]
    clean_data['completed'].value_counts()
    clean_data = clean_data[clean_data['completed'] == True]
    task_group_id = clean_data.groupby('joiner_id').sum().sort_values(
        'completed', ascending=False)
    completed = task_group_id.rename(columns={'completed':'Completed'})
    #print(completed)
    return completed

def pending_task():
    data = json_to_dataframe( url = f"http://service3-django:8010/task/")
    clean_data = data[["joiner_id", "completed"]]
    clean_data = clean_data[clean_data['completed'] == False]
    pending = clean_data[clean_data['completed']==False].groupby(
        ['joiner_id']).count().sort_values('completed', ascending=False)
    pending= pending.rename(columns={'completed':'Pending'})
    #print(pending)
    return pending

def top_joiners(completed_task):
    """ give the top five of joiners with more task completed"""
    #print(completed_task().sort_values('Completed', ascending=False).head())
    print(completed_task())
    print(type(completed_task))
    return completed_task().head()


def task_by_joiner():
    """give the csv file taht contains task by joiner"""
    completed = completed_task()
    pending = pending_task()
    task_by_joinerdf = pd.concat([completed, pending], axis=1)
    new_df = task_by_joinerdf.fillna(0).astype(int).sort_values(['Completed', 'Pending'], ascending=False)
    #print(new_df)
    return new_df

def task_by_X_joiner(id):
    """ give a report with details of a joiner and task completed and pending"""
    all_tasks  = task_by_joiner()
    filter_joiner = all_tasks.loc[[id]]
    #print(filter_joiner)
    return filter_joiner

def days_left_by_joiner():
    """ give a report that contains a report with days left to complete all the task pending"""
    data = json_to_dataframe( url = f"http://service3-django:8010/task/")
    clean_data = data[['joiner_id', 'estimated_required_hours', 'completed']]
    clean_data = data[['joiner_id', 'estimated_required_hours', 'completed']]
    clean_data = clean_data[clean_data['completed'] == False]
    clean_data = clean_data[['joiner_id', 'estimated_required_hours']]
    hours_left = clean_data.groupby('joiner_id').sum(
        'estimated_required_hours').sort_values(
            'estimated_required_hours', ascending=False)
    days_left = hours_left['estimated_required_hours'].div(8)
    days_left = days_left.to_frame().reset_index()
    days_left= days_left.rename(columns={'estimated_required_hours':'days_left'})
    return days_left

def pd_to_csv():
    df = days_left_by_joiner()
    stream = io.StringIO()
    df.to_csv(stream, sep=";")
    #print(stream.getvalue())
    return stream.getvalue()

#completed_task()
#pending_task()
top_joiners(completed_task)
#task_by_X_joiner(1128277285)
#pd_to_csv()
days_left_by_joiner()
"""
top_joiners()
task_by_X_joiner = take all of task, and filter for id and count completed task and no completed
task_by_joiner = "take all of task, and count task completed and not completed"""
