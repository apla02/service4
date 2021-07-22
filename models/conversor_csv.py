import pandas as pd
import io


def pd_to_csv(df):
    """convert a dataframe in a csv stream file like object"""
    stream = io.StringIO()
    df.to_csv(stream, sep=";", index=True)
    return stream
