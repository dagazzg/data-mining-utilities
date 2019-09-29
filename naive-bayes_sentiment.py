import nltk
import json
from nltk.stem.porter import *
from nltk.corpus import PlaintextCorpusReader
from gensim import corpora
from flask import request, jsonify, Flask, Response

##########
#Training#
##########
def train():
    # Reads in data, preprocesses and trains it in a Naive Bayes Classifier and returns the classifier object
    neg = PlaintextCorpusReader('C:\\Users\\Darren\\Downloads\\aclImdb\\train\\neg', '.+\.txt')
    pos = PlaintextCorpusReader('C:\\Users\\Darren\\Downloads\\aclImdb\\train\\pos', '.+\.txt')

    neg_docs1 = [neg.words(fid) for fid in neg.fileids()]
    pos_docs1 = [pos.words(fid) for fid in pos.fileids()]

    # Combine the categories of the corpus
    all_docs1 = neg_docs1 + pos_docs1
    num_neg_docs = len(neg_docs1)

    # Processsing for stopwords, alphabetic words, Stemming 
    all_docs2 = [[w.lower() for w in doc] for doc in all_docs1]
    print("lowering done")
    import re
    all_docs3 = [[w for w in doc if re.search('^[a-z]+$',w)] for doc in all_docs2]
    print("regex done")
    from nltk.corpus import stopwords
    stop_list = stopwords.words('english')
    all_docs4 = [[w for w in doc if w not in stop_list] for doc in all_docs3]
    print("stopword done")
    stemmer = PorterStemmer()
    all_docs5 = [[stemmer.stem(w) for w in doc] for doc in all_docs4]

    #Create dictionary
    dictionary = corpora.Dictionary(all_docs5)
    # print(dictionary)
    # Export as a text file to use with the pickled classifier
    dictionary.save_as_text("dictionary.txt")

    # Convert all documents to TF Vectors
    all_tf_vectors = [dictionary.doc2bow(doc) for doc in all_docs5]

    #Label the taining data. Since the folder name is the label, I use the same labels.
    all_data_as_dict = [{id:1 for (id, tf_value) in vec} for vec in all_tf_vectors]
    neg_data = [(d, 'negative') for d in all_data_as_dict[0:num_neg_docs-1]]
    pos_data = [(d, 'positive') for d in all_data_as_dict[num_neg_docs:]]
    all_labeled_data = neg_data + pos_data

    #Generate the trained classifier
    #Can use max entropy as well
    classifier = nltk.NaiveBayesClassifier.train(all_labeled_data)
    return classifier, dictionary

#######
#Using#
#######
def classify(classifier, dictionary, data):
    #Requires data passed in as a list of strings. 1 string = 1 review
    #Returns a list of labels as json
    stemmer = PorterStemmer()
    # Text pre-processing, including stop word removal, stemming, etc.
    all_valid_docs = [review.split(" ") for review in data]
    all_valid_docs2 = [[w.lower() for w in doc] for doc in all_valid_docs]
    all_valid_docs3 = [[w for w in doc if re.search('^[a-z]+$',w)] for doc in all_valid_docs2]
    all_valid_docs4 = [[w for w in doc if w not in stop_list] for doc in all_valid_docs3]
    all_valid_docs5 = [[stemmer.stem(w) for w in doc] for doc in all_valid_docs4]

    # Note that we're using the dictionary created while training the classifier
    all_valid_tf_vectors = [dictionary.doc2bow(doc) for doc in all_valid_docs5]

    # Convert documents into dict representation.
    all_valid_data_as_dict = [{id:1 for (id, tf_value) in vec} for vec in all_valid_tf_vectors]

    predicted_labels = []
    for review in all_valid_data_as_dict:
        predicted_labels.append(str(classifier.classify(review)))

    resp = json.dumps({'response': predicted_labels})
    return resp


nb_classifier, tf_dictionary = train()