from models.validations import Validation
from collections import OrderedDict
import csv
import pandas as pd


class Query(Validation):
    """class to handle different querys to make a reports of new joiners"""

    def completed_task(self):
        """ give the task completed by joiner"""
        data = self.json_to_dataframe()
        print(data)
        clean_data = data[["joiner_id", "completed"]]
        clean_data['completed'].value_counts()
        clean_data = clean_data[clean_data['completed'] == True]
        task_group_id = clean_data.groupby('joiner_id').sum().sort_values(
            'completed', ascending=False)
        completed = task_group_id.rename(columns={'completed':'Completed'})
        #print(completed)
        return completed

    def pending_task(self):
        """return a dataframe with ask pendindg by joiner"""
        data = self.json_to_dataframe()
        clean_data = data[["joiner_id", "completed"]]
        clean_data = clean_data[clean_data['completed'] == False]
        pending = clean_data[clean_data['completed']==False].groupby(
            ['joiner_id']).count().sort_values('completed', ascending=False)
        pending= pending.rename(columns={'completed':'Pending'})
        #print(pending)
        return pending

    def top_joiners(self):
        """ give the top five of joiners with more task completed"""
        #print(completed_task().sort_values('Completed', ascending=False).head())
        top = self.completed_task().head()
        return top


    def task_by_joiner(self):
        """give the csv file taht contains task by joiner"""
        completed = self.completed_task()
        pending = self.pending_task()
        task_by_joinerdf = pd.concat([completed, pending], axis=1)
        new_df = task_by_joinerdf.fillna(0).astype(int).sort_values(
            ['Completed', 'Pending'], ascending=False)
        #print(new_df)
        return new_df

    def task_by_X_joiner(self, id):
        """ give a report with details of a joiner and task completed and pending"""
        try:
            all_tasks  = self.task_by_joiner()
            filter_joiner = all_tasks.loc[[id]]
            #print(filter_joiner)
            return filter_joiner
        except Exception:
            return {'message': "joiner id not found"}

    def days_left_by_joiner(self):
        """ give a report that contains a report with days left to complete all the task pending"""
        data = self.json_to_dataframe()
        clean_data = data[['joiner_id', 'estimated_required_hours', 'completed']]
        clean_data = data[['joiner_id', 'estimated_required_hours', 'completed']]
        clean_data = clean_data[clean_data['completed'] == False]
        clean_data = clean_data[['joiner_id', 'estimated_required_hours']]
        hours_left = clean_data.groupby('joiner_id').sum(
            'estimated_required_hours').sort_values(
                'estimated_required_hours', ascending=False)
        days_left = hours_left['estimated_required_hours'].div(8)
        days_left = days_left.to_frame()
        days_left= days_left.rename(columns={'estimated_required_hours':'days_left'})
        return days_left
