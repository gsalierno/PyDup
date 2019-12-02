import re
from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def readDictFromFile(path):
    dict = {}
    with open(path) as dict_file:
        for line in dict_file:
            chunk = line.split(',"')
            answ = cleanAndSplitAnswer(chunk[1])
            answ = answ.split(',\'')
            dict[chunk[0]] = answ
    return dict


def cleanAndSplitAnswer(a):
    a = a.replace('[', "")
    a = a.replace("]", "")
    if a.startswith("'") and a.endswith("'"):
        a = a[1:-1]
    return a


def printDictionary(questions):
    for k in questions.keys():
        print("QUESTION: ", k, "ANSWERS: ", questions[k])


def sent_vectorizer(sent, model):
    sent_vec = []
    numw = 0
    for w in sent:
        try:
            if numw == 0:
                sent_vec = model[w]
            else:
                sent_vec = np.add(sent_vec, model[w])
            numw += 1
        except:
            pass

    return np.asarray(sent_vec) / numw


def clean_quest(questions):
    tokenizer = nltk.data.load('tokenizers/punkt/italian.pickle');
    sent = []
    for q in questions:
        # Normalize tabs and remove newlines
        no_tabs = str(q).replace('\t', ' ').replace('\n', '')
        # Remove all characters except A-Z and a dot.
        alphas_only = re.sub("[^a-zA-Z\.]", " ", no_tabs);
        # Normalize spaces to 1
        multi_spaces = re.sub(" +", " ", alphas_only);
        # Strip trailing and leading spaces
        no_spaces = multi_spaces.strip();
        # Normalize all charachters to lowercase
        clean_text = no_spaces.lower();
        # Get sentences from the NLTK tokenizer, remove the dot in each.
        sentences = word_tokenize(clean_text)
        sentences = [re.sub("[\.]", "", sentence) for sentence in sentences]
        sent.append(sentences)
    return sent


questions = readDictFromFile('../questions_raw_cleaned.txt')

# CLUSTER ANALYSIS WITH WORD EMBEDDINGS AT SENTENCE LAYER

# PREPROCESSING
sentences = clean_quest(list(questions.keys()))
# TRAIN WORD2VEC MODEL
model = Word2Vec(sentences, min_count=2)
X = []
for sentence in sentences:
    X.append(sent_vectorizer(sentence, model))
print("========================")
# CLUSTERING WITH K-MEANS
NUM_CLUSTERS = 5
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance)
assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
print(assigned_clusters)

for index, sentence in enumerate(sentences):
    print(str(assigned_clusters[index]) + ":" + str(sentence))
