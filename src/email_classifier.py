import string
import math

from email_parser import EmailCSVParser

class SpamClassification:
    def __init__(self, training_data):

        self.training_data = training_data
        self.spam = 0
        self.ham = 0
        self.unique_words = {}
        self.total_spam_words = 0
        self.total_ham_words = 0
        self.spam_words = {}
        self.ham_words = {}


        self.train()

    def train(self):
        parser = EmailCSVParser()
        result = parser.parse(self.training_data)
        print('Finished training with data from', self.training_data)
        self.spam = result.get('spam')
        self.ham = result.get('ham')
        self.unique_words = result.get('unique_words')
        self.total_spam_words = result.get('total_spam_words')
        self.total_ham_words = result.get('total_ham_words')
        self.spam_words = result.get('spam_words')
        self.ham_words = result.get('ham_words')

    def log_p_words_given_spam(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())
        for word in email:
    
            nominator = (self.spam_words.get(word) or 0) + 1
    
            denominator = self.total_spam_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def log_p_words_given_ham(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())
        for word in email:
    
            nominator = (self.ham_words.get(word) or 0) + 1
    
            denominator = self.total_ham_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def clean(self, email):
        file = open(email, 'r')
        lines = file.readlines()

        all_words = []

        for line in lines:
    
            m = line.lower()
    
            m = m.translate(str.maketrans('', '', string.punctuation))
    
            m = m.translate(str.maketrans('', '', string.digits))
            words = m.split()
            all_words += words

        return all_words

    def classify(self, email):
        cleaned_email = self.clean(email)

        log_p_spam = math.log(self.spam / (self.spam + self.ham))
        log_p_ham = math.log(self.ham / (self.spam + self.ham))
        log_p_words_given_spam = self.log_p_words_given_spam(cleaned_email)
        log_p_words_given_ham = self.log_p_words_given_ham(cleaned_email)
        log_probability_of_spam = log_p_spam + log_p_words_given_spam
        log_probability_of_ham = log_p_ham + log_p_words_given_ham

        return log_probability_of_spam > log_probability_of_ham