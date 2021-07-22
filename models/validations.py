import requests
import json
from collections import OrderedDict
import csv
import pandas as pd

class Validation():
    """class to convert an json object in a dtaframe to be processed to make reports"""

    def __init__(self, url):
        """instation of a class, receive a url of the another microservice"""
        self.url = url

    def get_object(self):
        "method to collect data using web scraping from the microservice 3"
        try:
            r = requests.get(self.url)
            json_object = json.loads(r.text)
            return json_object
        except Exception:
            print("invalid url")


    def json_to_dataframe(self):
        """converts a json object in a dataframe"""
        o_json = self.get_object()
        dataframe = pd.DataFrame(o_json)
        blankIndex=[''] * len(dataframe)
        dataframe.index=blankIndex
        #print(dataframe)
        return dataframe
