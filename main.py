from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, defaultdict
from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import logging
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = Word2Vec.load_word2vec_format("new.model.bin", binary=True)
w2v = dict(zip(model.index2word, model.syn0))


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
                np.mean([self.word2vec[w] * self.word2weight[w]
                         for w in words if w in self.word2vec] or
                        [np.zeros(self.dim)], axis=0)
                for words in X
            ])

etree_w2v_tfidf = Pipeline([
    ("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),
    ("extra trees", ExtraTreesClassifier(n_estimators=200))])

# CORPUS FROM TEXT STRINGS
corpus = [None] * 25000
classes = [None] * 25000

pos = open("train-pos.txt")
neg = open("train-neg.txt")

for i in range(12500):
    corpus[i] = pos.readline()
    corpus[i + 12500] = neg.readline()
    classes[i] = "positive"
    classes[i + 12500] = "negative"


pos.close()
neg.close()
typeOfString = [None] * 1


etree_w2v_tfidf.fit(corpus, classes)
def apply_string(str_classify):
    typeOfString[0] = str_classify
    result = etree_w2v_tfidf.predict(typeOfString)[0]
    return result



