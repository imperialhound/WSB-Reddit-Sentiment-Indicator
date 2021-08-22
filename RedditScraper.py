from psaw import PushshiftAPI
import pandas as pd
import time


def collect_subreddit_comments(after='60d', subreddit='wallstreetbets', columns=['body', 'score', 'created_utc']):
    """
    :param str after: Number of days to go in the past
    :param str subreddit: subreddit to collect comments from
    :param list columns: parameters to collect from comments
    :return: df: dataframe of collected subreddit comments
    :rtype: DataFrame
    """

    # connect to PushShift reddit api
    api = PushshiftAPI()

    # Create subreddit comment generator
    gen = api.search_comments(after=after, subreddit=subreddit, filter=columns)

    # loop through generator and append to dataframe
    start = time.time()
    df = pd.DataFrame([thing.d_ for thing in gen])
    end = time.time()
    print("time to download data:", end - start)

    return df
