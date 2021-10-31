# TEXT_ANALYSIS USING TF-IDF

# PACKAGE INSTALL
# https://www.codegrepper.com/code-examples/python/run+pip+install+from+python+script
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install('imdbpie')

# IMPORTS
from imdbpie import Imdb
import string
import pprint
import math


# RETRIEVING DATA
imdb = Imdb()
reviews = imdb.get_title_user_reviews("tt0245429")
# print(imdb.search_for_title('spirited away'))
# pprint.pprint(reviews.keys())
# pprint.pprint(reviews['base'])


# PROCESS DATA
def reviews_to_list(reviews):
    """
    input: dictionary from imdb
    output: list of reviews, known as corpus
    """
    l = []
    for item in reviews["reviews"]:
        content = item["reviewText"]
        l.append(content)
    return l

def clean_words_to_list(text):
    l = []
    f = text.replace("-", " ")
    for word in f.split():
        t = word
        t = t.strip(string.whitespace + string.punctuation)
        t = t.lower()
        l.append(t)
    # To fix bad puncuation incl. ".,/"
    for word in l:
        if "." in word:
            l.remove(word)
            x = word.split(".")
            for item in x:
                l.append(item)
    for word in l:
        if "," in word:
            l.remove(word)
            x = word.split(",")
            for item in x:
                l.append(item)
    for word in l:
        if "/" in word:
            l.remove(word)
            x = word.split("/")
            for item in x:
                l.append(item)
    return l


# TEXT AND WORD ANALYSIS
def count_words(text):
    d = {}
    all_words = clean_words_to_list(text)
    for word in all_words:
        if word not in d:
            d[word] = 1
        else:
            d[word] += 1
    return d

def unique_words(text):
    """
    returns a list of unqiue words from a text
    """
    l = []
    all_words = clean_words_to_list(text)
    for word in all_words:
        if word not in l:
            l.append(word)
    return l

def unique_words_corpus(corpus):
    """
    input: a list of all texts
    returns: list of unique words from a corpus
    """
    l = []
    all_reviews = []
    for item in corpus:
        f = clean_words_to_list(item)
        all_reviews.append(f)
    for review in all_reviews:
        for word in review:
            if word not in l:
                l.append(word)
    return l


# TF-IDF ANALYSIS -- Learned all tf-idf functions through -> https://en.wikipedia.org/wiki/Tf%E2%80%93idf
def term_frequency_dict(text):
    """
    returns the term frequency of one word as float
    """
    d = {}
    f = clean_words_to_list(text)
    for word in f:
        if word not in d:
            d[word] = f.count(word) / len(f)
    return d

def inside_list(word, list):
    if word in list:
        return True

def inverse_def_frequency(word, corpus):
    """
    word is the target word
    corpus is the list of all reviews
    """
    word_list = []
    count = 0
    for item in corpus:
        f = clean_words_to_list(item)
        word_list.append(f)
    for item in word_list:
        if inside_list(word, item):
            count += 1
    idf = math.log(len(corpus) / count)
    return idf

def idf_dict(corpus):
    """
    returns the idf constant of all words in a corpus
    """
    d = {}
    unique = unique_words_corpus(corpus)
    for item in unique:
        if item not in d:
            d[item] = inverse_def_frequency(item, corpus)
    return d

def tfidf_dict(corpus):
    idf = idf_dict(corpus)
    all_tfidf = []
    for item in corpus:
        tfidf = {}
        tf = term_frequency_dict(item)
        unique = unique_words(item)
        for word in unique:
            x = tf[word] * idf[word]
            tfidf[word] = x
        all_tfidf.append(tfidf)
    return all_tfidf


# WRAP-UP
def most_frequent(corpus, n):
    f = tfidf_dict(corpus)
    frequent_word_list = []
    for review in f:
        l = []
        for item in review.items():
            l.append(item)
        l.sort(key=lambda x: x[1], reverse=True)
        for item in l[:n]:
            frequent_word_list.append(item[0])
    return frequent_word_list

def common_words(words):
    d = {}
    final = []
    for item in words:
        d[item] = d.get(item, 0) + 1
    for item in d.items():
        final.append(item)
    final.sort(key=lambda x: x[1], reverse=True)
    print(f'# Times   Word')
    print(f'-------   ----------')
    for item in final:
        print(f'   {item[1]}      {item[0]}')


# TEST CODE
def main():
    all_reviews = reviews_to_list(reviews)
    frequent_words = most_frequent(all_reviews, 30)
    common_words(frequent_words)

if __name__ == "__main__":
    main()
