import pandas as pd

# TODO: make this class universal to all financial assets, currently limited


wish_list = ['$wish', 'wish', 'contextlogic']
spy_list = ['$spy', 'spy','s&p', 'spdr']
clov_list = ['$clov', 'clov', 'clover health']
hood_list = ['$hood', 'hood', 'robinhood', 'robin']
bb_list = ['$bb', 'bb', 'blackberry']
srne_list = ['$srne', 'srne', 'sorrento']
whks_list = ['$wkhs', 'wkhs', 'workhorse']
sofi_list = ['$sofi', 'sofi']
tsla_list= ['$tsla', 'tesla', 'elon', 'musk']
clne_list = ['$clne', 'clne', 'clean energy fuels']
spce_list = ['$spce', 'spce', 'virgin galactic']
clf_list = ['$clf', 'clf', 'cleveland cliff']
gme_list = ['$gme', 'gme', 'gamestop', 'game stop']
amc_list = ['$amc', 'amc', 'american multinational', 'entertainment holdings']
body_list = ['$body', 'body', 'beachbody']
pltr_list = ['$pltr', 'pltr', 'palantir']
baba_list = ['$baba', 'baba', 'alibaba']
tlry_list = ['$tlry', 'tlry', 'tilray']


class WSBStockParser:

    def __init__(self):
        self.assign_tickers()

    def assign_tickers(self, tickers=None):
        """ Assigns ticker attribute

        :param dict tickers: dictionary of tickers
        :return: assign ticker_dict attribute
        """
        if tickers is None:

            self.ticker_dict = {'wish':wish_list, 'spy':spy_list, 'clov': clov_list, 'hood':  hood_list,
                  'bb': bb_list, 'srne': srne_list, 'whks': whks_list, 'sofi': sofi_list,
                  'tsla':tsla_list, 'clne': clne_list, 'spce' : spce_list, 'clf': clf_list,
                  'gme' : gme_list, 'amc': amc_list, 'body': body_list, 'pltr': pltr_list,
                  'baba' : baba_list, 'tlry' : tlry_list }

        else:
            self.ticker_dict = tickers

    def find_tickers(self, df):
        """ Find all instances of #tickers in wallstreetbet comments

        :param DataFrame df: find tickers on WSB
        :return top_tickers: top list of tickers found
        :rtype: list
        """

        # Finding all tickers mentioned in body
        df['tickers'] = df['body'].str.lower().str.extract("\$([A-Za-z]+)")
        data_ticker_analysis = df[df['tickers'].notnull()]

        # Display top twenty most mentioned ticker codes on WSB
        top_tickers = data_ticker_analysis['tickers'].value_counts()

        return top_tickers

    def find_mentions(self, df):
        """ Find all mentions within WSB bets from ticker_dict attribute
        and assigns column based on mention

        :param DataFrame df: dataframe containing WSB comments
        :return df_stocks: df with new stock column
        :rtype: DataFrame
        """

        # Create empty dataframe to populate with data
        df_stocks = pd.DataFrame()

        for stock in self.ticker_dict.keys():
            print(f"find mentions of ticker {stock}")
            df_tick = df.loc[df['body'].str.contains("|".join(self.ticker_dict[stock]), case=False)]
            df_tick['Stock'] = stock
            df_stocks = df_stocks.append(df_tick)

        print(f"{df_stocks.shape[0]} individual comments of select stocks")

        return df_stocks





