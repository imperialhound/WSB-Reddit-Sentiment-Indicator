import re
import string
import datetime


class Preprocessor:

    @staticmethod
    def __preprocess_chain(text):
        """clean string by removing unnecessary content

        :param str text: string to do data cleaning
        :return text: string cleaned
        :rtype: str
        """
        # Remove Emails
        text = re.sub('\S*@\S*\s?', '', text)

        # Remove new line characters
        text = re.sub('\s+', ' ', text)

        # Remove distracting single quotes
        text = re.sub("\'", "", text)

        # Remove any and all punctuations
        p = re.compile("[" + re.escape(string.punctuation) + "]")
        text = re.sub(p, ' ', text)

        # Remove any digits
        text = re.sub('\d+', '', text)

        # Remove Extra Whitespace
        text = re.sub(' +', ' ', text)

        return text.lower()

    @staticmethod
    def __apply_datetime(df, date='created_utc'):
        """apply date, month and day datetime variables

        :param DataFrame df: dataframe to apply datetime variables to
        :param str date: name of epoch dateime variable to convert
        :return df: dataframe with datetimes applied
        :rtype: DataFrame
        """
        assert date in df.columns, 'assigned date column not present change date parameter'

        df['date'] = df.apply(lambda row: datetime.datetime.utcfromtimestamp(row[date]).strftime('%Y-%m-%d %H'), axis=1)

        df['month'] = df.apply(lambda row: datetime.datetime.utcfromtimestamp(row[date]).strftime('%m'), axis=1)

        df['day'] = df.apply(lambda row: datetime.datetime.utcfromtimestamp(row[date]).strftime('%d'), axis=1)

        return df

    def preprocess_reddit(self, df):
        """apply text preprocessing and datetime variables

        :param DataFrame df: dataframe to preprocess
        :return df: dataframe with datetimes applied
        :rtype: DataFrame
        """
        print('Before preprocess dataframe shape', df.shape)

        df = df[['body', 'score', 'created_utc']]

        # Remove all removed comments
        df = df[~(df['body'] == '[removed]')]
        df = df[~(df['body'] == '[deleted]')]
        df = df.dropna()
        print('Data after removing removed comments', df.shape)

        # edgecase - common on wallstreetbets
        df = df[~(df['body'] == 'hmsthinkingmeat')]

        # loop through columns and apply text preprocessing
        df['body'] = df['body'].apply(lambda x: self.__preprocess_chain(x))

        df = self.__apply_datetime(df)

        print('After preprocess dataframe shape', df.shape)

        return df

