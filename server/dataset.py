import numpy as np
import os
from collections import defaultdict
from download import main_page, db
import json
import requests


collection = db[main_page]

# # Setup flask server
# app = Flask(__name__)

# # Setup url route which will send the json data
# @app.route('/api/topics', methods)

class DataSet:
    
    y_words=[]
    def __init__(self,dirname=collection,
                 length_limit=3,
                 count_limit=20):
        # lower bound on length of word
        self.length_limit = length_limit
        # lower limit on min occurences in dataset
        self.count_limit = count_limit

        self.titles = []
        self.pages = []
        self._load_data(dirname)
        self._load_stopwords()
        self._make_word_list()

        self.page_count = len(self.pages)
        self.word_count = len(self.words)

        self._pages_to_vectors()

    def _load_data(self,dirname):
        """Read all txt files in the dirname directory."""
        col = collection.find()
        for page in col:
            pageid,title,text = page['_id'],page['title'],page['text']
            text_tm = [ word.lower() for word in text.split() ]
            self.pages.append(text_tm)
            self.titles.append(title)
            

    def _load_stopwords(self,filename="stopwords"):
        """Read list of stopwords."""
        with open(filename,'r') as f:
            lines = f.readlines()
        self.stopwords = [ line.strip() for line in lines ]

    def _make_word_list(self):
        """Find all unique words in the corpus."""

        # count the occurences of every word
        word_counts = defaultdict(lambda: 0)
        for page in self.pages:
            for word in page:
                word_counts[word] += 1

        for word in list(word_counts):
            if len(word) < self.length_limit:
                # skip short words
                del word_counts[word]
            elif word in self.stopwords:
                # skip common words (stopwords)
                del word_counts[word]
            elif word_counts[word] < self.count_limit:
                # skip words that appear only a few times
                del word_counts[word]

        # list of words
        self.words = sorted(list(word_counts))
        # map from word to index in sorted list
        self.word_index = { w:i for i,w in enumerate(self.words) }
        # set of words (fast lookup)
        self.word_set = set(self.words)

    def _page_to_vector(self,page):
        """convert a single page to a vector of word counts"""
        page = [ word for word in page if word in self.word_set ]
        indices = [ self.word_index[word] for word in page ]
        vector = np.bincount(indices)
        vector.resize(self.word_count)
        # AC: you need to set refcheck=False if you want to debug
        #vector.resize(self.word_count,refcheck=False)
        return vector

    def _pages_to_vectors(self):
        """convert all pages to a vector of word counts"""
        vectors = [ self._page_to_vector(page) for page in self.pages ]
        self.vectors = np.array(vectors)


    def get_word_probability_table(self,pr,header,length=20):
        """Return a list of word probability tuples.
           Return the top most probable words, based on length"""
        word_pr = [(w, p) for w, p in enumerate(pr)]
        word_pr.sort(key=lambda x: x[1], reverse=True)
        return [(self.words[w], p) for w, p in word_pr[:length]]


    def print_common_words(self):
        """print list of most frequently appearing words"""
        counts = self.vectors.sum(axis=0)
        total = counts.sum()
        pr = [ c/total for c in counts ]

        header = "common words (out of %d total)" % total

        self.get_word_probability_table(pr,header)

    def index_to_word(self, index):
        """Return the word corresponding to the given index."""
        return self.words[index]

