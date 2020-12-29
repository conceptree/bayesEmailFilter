import string
import math

from email_parser import EmailParser

class SpamClassification:
    def __init__(self, trainingDB):

        self.trainingDB = trainingDB
        self.types = ['spam','ham','unique_words', 'total_spam_words', 'spam_words', 'ham_words']
        self.spam, self.ham, self.total_spam_words, self.total_ham_words = 0
        self.unique_words, self.spam_words, self.ham_words = {}
        self.train()

    def train(self):
        parser = EmailParser()
        result = parser.parse(self.trainingDB)
        print('Finished training with data from', self.trainingDB)
        
        for type in types:
            self[type] = result.get(type)

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