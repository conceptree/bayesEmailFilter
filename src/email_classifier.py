import string
import math
from email_parser import EmailParser
from chart import ChartPrompt

class EmailClassifier:
    def __init__(self):

        self.trainingDB = '../data/spam_ham_dataset.csv'
        self.types = ['spam', 'ham', 'unique_words', 'total_spam_words',
                      'total_ham_words', 'spam_words', 'ham_words']
        self.spam = self.ham = self.total_spam_words = self.total_ham_words = 0
        self.unique_words = self.spam_words = self.ham_words = {}
        self.train()

    def train(self):
        parser = EmailParser()
        result = parser.parse(self.trainingDB)

        for type in self.types:
            request = result.get(type)
            if(type == 'spam'):
                self.spam = request
            if(type == 'ham'):
                self.ham = request
            if(type == 'unique_words'):
                self.unique_words = request
            if(type == 'total_spam_words'):
                self.total_spam_words = request
            if(type == 'total_ham_words'):
                self.total_ham_words = request
            if(type == 'spam_words'):
                self.spam_words = request
            if(type == 'ham_words'):
                self.ham_words = request

        print('----- TRAINING RESULTS -----')
        print('Spam emails: '+str(self.spam))
        print('Ham emails: '+str(self.ham))
        print('Unique words in the vocabulary: ' +
              str(len(self.unique_words.keys())))
        print('Total words in spam emails: '+str(self.total_spam_words))
        print('Total words in ham emails: '+str(self.total_spam_words))
        print('Occurrences for each word in spam emails: ' +
              str(len(self.spam_words.keys())))
        print('Occurrences for each word in ham emails: ' +
              str(len(self.ham_words.keys())))
        print('Training complete! Source:', self.trainingDB)
        
        chart = ChartPrompt()
        xVals = [0, 1, 2, 3, 4, 5, 6]
        yVals = [self.spam, self.ham, len(self.unique_words.keys()), self.total_spam_words, self.total_spam_words, len(self.spam_words.keys()), len(self.ham_words.keys())]
        yLabels = ['Spam emails', 'Ham emails', 'Unique Words', 'Total in Spam', 'Total in Ham', 'Occur. Spam', 'Occur. Ham']
        chart.showChart(xVals, yVals, 'Training Results', 'Classifications', 'Descriptions', yLabels)

    def prob_words_given_spam(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())

        for word in email:
            nominator = (self.spam_words.get(word) or 0) + 1
            denominator = self.total_spam_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def prob_words_given_ham(self, email):
        sum = 0
        num_unique_words = len(self.unique_words.keys())
        for word in email:
            nominator = (self.ham_words.get(word) or 0) + 1
            denominator = self.total_ham_words + num_unique_words
            sum += math.log(nominator / denominator)

        return sum

    def clean(self, type, email):
        if(type == 'string'):
            lines = email.splitlines()
        elif(type == 'file'):
            file = open(email, 'r')
            lines = file.readlines()

        all_words = []

        for line in lines:
            message = line.lower()
            message = message.translate(
                str.maketrans('', '', string.punctuation))
            message = message.translate(str.maketrans('', '', string.digits))
            words = message.split()
            all_words += words

        return all_words

    def classify(self, type, email):
        cleaned_email = self.clean(type, email)

        prob_spam = math.log(self.spam / (self.spam + self.ham))
        prob_ham = math.log(self.ham / (self.spam + self.ham))
        prob_words_given_spam = self.prob_words_given_spam(cleaned_email)
        prob_words_given_ham = self.prob_words_given_ham(cleaned_email)
        probability_of_spam = prob_spam + prob_words_given_spam
        probability_of_ham = prob_ham + prob_words_given_ham

        print('Probability of being spam:',prob_spam)
        print('Probability of not being spam:',prob_ham)
        print('Probability of used words in spam emails:',prob_words_given_spam)
        print('Probability of used words not in spam emails:',prob_words_given_ham)
        if(prob_words_given_ham > prob_words_given_spam):
            spamAndHamWordsDifference = prob_words_given_ham - prob_words_given_spam
        else:
            spamAndHamWordsDifference = prob_words_given_spam - prob_words_given_ham
        print('Words not in the DB:', str(spamAndHamWordsDifference))
        print('Final result:', abs(probability_of_spam) > abs(probability_of_ham))
        
        if(abs(probability_of_spam) > abs(probability_of_ham)):
            print('This message is considered a spam!')
        else:
            print('This message is not considered a spam!')

def main():
    print('------- Welcome to the Email Classifier Engine -------')
    print('Training the algorithm...')
    emailClassifier = EmailClassifier()
    userInput = input('Want to classify an email? (y/n) :')
    if(userInput == 'y'):
        print('----- Email Classifier Menu -----')
        print('1. Type the email?')
        print('2. Type an email file path?')
        print('3. Go Back')
        userInput = input('Choose 1 or 2:')
        if(userInput != "" or userInput != " "):
            if(userInput == "1"):
                userInput = input('Type your email here: ')
                if(userInput != '' or userInput != " "):
                    emailClassifier.classify("string", userInput)
            elif(userInput == "2"):
                userInput = input('What to use the available source file? (y/n) :')
                if(userInput == "y"):
                    emailClassifier.classify("file","../data/testMail.txt")
                elif(userInput == "n"):
                    userInput = input("Please enter the source path for your email txt file, or, type back:")
                    if(userInput == "back"):
                        main()
                    elif(userInput == "" or userInput == " "):
                        print("Not a valid selection, please try again!")
                        main()
                    else:
                        emailClassifier.classify("file",userInput)
            elif(userInput == "3"):
                main()
            else:
                print('Not a valid selection, please try again!')
                main()
        else:
            print('Not a valid selection, please try again!')
            main()
    else:
        exit

if __name__ == "__main__":
    main()
