import sys
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import os

#ps = PorterStemmer()


class Sentiment(ClassifierI):
    
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

def find_features(document):
    #print("Cleaning Input text...")
    document = re.sub(r'[^(a-zA-Z)\s]','', document)
    #print("Result after cleaning : ",document)
    words = word_tokenize(document)
    k = nltk.pos_tag(words)
    #print("Tokenization Results :",words)
    #print("Loading stop words from nltk")
    stop_words = list(set(stopwords.words('english')))
    #print("Eliminating Stop words from input string...")
    words = [w for w in words if not w in stop_words] 
    #print("Resultant list of words : ",words) 
    #print("Filtering adjectives using POS tagging...")
    allowed_word_types = ["JJ"]
    words = []
    for w in k:
        if w[1] in allowed_word_types:
            words.append(w[0].lower())   
    #print("Resultant after filtering : ",words)
    features = {}
    k = open('all_words.pickle','rb')
    all_words = pickle.load(k)
    k.close()
    all_words = nltk.FreqDist(all_words)
    #print("Loading dictionary : (first 5 shown) ",list(all_words)[:5])
    #print()
    word_features = list(all_words.keys())
    #print("Matching with dictionary and assigning True if present otherwise False")
    for w in word_features:
        features[w] = (w in words)
    return features

def load_model(file_path): 
    classifier_f = open(file_path, "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    return classifier

def sentiment(text):
    #print("Loading prediction model...")
    MNB_Clf = load_model('MNB_clf.pickle')
    ensemble_clf = Sentiment(MNB_Clf)
    #print("Processing your text...") 
    feats = find_features(text)
    #print("Features extracted and inputted to model: (first 5 shown)",end=' ')
    #j=0
    #for i in feats:
    #	print(i,":",feats[i],";",end=' ')
    #	j+=1
    #	if (j>5):
    #		break
    #print()
    return ensemble_clf.classify(feats), ensemble_clf.confidence(feats)
import sys
def senti(st):
    #sent = sys.argv[1]
    #print("Your sentence was : "+sent)
    #dic = {'pos':'positive','neg':'negative'}
    #print("Prediction model says that the text is "+dic[sentiment(sent)[0]])
    return sentiment(st)[0]
def main():
    chatbot=''
    trainer=''
    try:
        from chatterbot import ChatBot
        from chatterbot.trainers import ChatterBotCorpusTrainer
        chatbot=ChatBot('Ron Obvious')
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train("chatterbot.corpus.english")
    except:
        try:
            from chatterbot import ChatBot
            from chatterbot.trainers import ChatterBotCorpusTrainer
            chatbot=ChatBot('Ron Obvious')
            trainer = ChatterBotCorpusTrainer(chatbot)
            trainer.train("chatterbot.corpus.english")
        except:
            print("Error Occurred")
            sys.exit(0)
    print()
    print()
    print()
    print("Welcome to Chat Trainer Agent.")
    print("'Talk to the chatbot and get your chat evaluated.'")
    print("This agent aims to improve your chatting skills...")
    print("Enter EXIT to end training...")
    print()
    print("Start the conversation!!! All the best!!!")
    usr = ""
    posc = 0
    negc = 0
    while True:
        print("USER : ",end=' ')
        usr = input()
        if usr.lower()=="exit":
            break
        if senti(usr)=="pos":
            posc+=1
        else:
            negc+=1
        print("BOT : "+str(chatbot.get_response(usr)))
    f = open('highscore.pickle','rb')
    highsc = pickle.load(f)
    f.close()
    currsc = posc-negc
    if currsc>highsc:
        f = open('highscore.pickle','wb')
        pickle.dump(currsc,f)
        f.close()
    print()
    print("Summary Report : ")
    print("Positive Sentences : ",posc)
    print("Negative Sentences : ",negc)
    print("Your Score : ",currsc)
    print("Previous High Score : ",highsc)
if __name__=="__main__":
    os.chdir(os.path.abspath(__file__)[:-14])
    main()