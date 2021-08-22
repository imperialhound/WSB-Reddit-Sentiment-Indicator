from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Vader:

    nltk.download('vader_lexicon')

    def __init__(self):
        self.sentiment = SentimentIntensityAnalyzer()

    def classify(self, text):
        """generate sentiment scores utilize vader lexicon
        Args:
            text (string): text to be classified
        Returns:
            score (float): score from -1 to 1 on sentiment
        """

        score = self.sentiment.polarity_scores(text)["compound"]

        return score

    def classify_list(self, df, column='body'):
        """classify all text within a column
        Args:
            df (DataFrame): dataframe contains column to generate sentiment
            column (string): name of column
        return:
            df (DataFrame): dataframe with new sentiment column
        """

        assert df[column].dtypes == 'object', 'column type must be string'

        # Create vader sentiment column
        df['vader_sentiment'] = df.apply(lambda row: self.classify(row.body), axis=1)

        # add weighted sentiment if score is present
        if "score" in df.columns:
            df['weighted_sentiment'] = df['score'] * df['vader_sentiment']

        return df


class OpinionatedRoberta:
    
    def __init__(self, task='sentiment', truncation=100):
        self.task = task # emoji, emotion, hate, irony, offensive, sentiment, stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary
        self.truncation = truncation 
        self.model_endpoint = f"cardiffnlp/twitter-roberta-base-{self.task}"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_endpoint)
        self.initiate_model()
    
    def initiate_model(self, store=True):
        """Responsible for setting the model attribute by downloading
        huggingface Roberta model and then storing it locally
        Args:
            store (bool): True to store the model locally in directory
        """
        
        # Download Roberta model from huggingface and set model attribute
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_endpoint)
        
        # Save Model
        if store is True:
            self.model.save_pretrained(self.model_endpoint)
    
    def __truncate_text(self, text):
        """Truncates any string to specified limit of words to lower dimensions
        Args:
            text (string): string to be truncated 
        """
        
        # Truncate text to limit out of bounds error 
        new_text = text.split(" ")[:self.truncation]
    
        return " ".join(new_text)
    
    def classify(self, text):
        """classify text into labels based on roberto task
        Args:
            text (string): string to be classified
        return 
            scores (int): int represent classification label 
        """
        
        text = self.__truncate_text(text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        return scores
    
    def classify_list(self, df, column='body'):
        """classify all text within a column
        Args:
            df (DataFrame): dataframe contains column to generate sentiment 
            column (string): name of column
        return:
            df (DataFrame): dataframe with new sentiment column
        """
        # 0 (negative), 1 (neutral), 2 (positive)
    
        assert df[column].dtypes == 'object', 'column type must be string'
        
        scores = []

        for comment in df[column].values:

            try:
                sentiment_probs = list(self.classify(comment))
                prediction = sentiment_probs.index(max(sentiment_probs))
                scores.append(prediction)

            except:
                # if edgecase occurs output neutral sentiment 
                scores.append(1)
        
        # create new column of sentiment scores 
        df['bert_sentiment'] = scores
        
        return df
