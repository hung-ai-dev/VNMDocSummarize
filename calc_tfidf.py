import math
import string
import re
import io
import sklearn
from os import listdir
from os.path import isfile, join
from pyvi.pyvi import ViTokenizer as viToken

from summa.preprocessing import vnm_text_cleaner

def read_file_from_folder(url_folder):
    files = listdir(url_folder)
    corpus = ''
    cnt = 0
    for file_name in files:
        file_dir = join(url_folder, file_name)
        f = open(file_dir, 'r')
        corpus += f.read()
    return corpus

def build_dictionnary(corpus):
    dictionary = []
    file = io.open('/media/hung/Data/NLP/textrank/summa/preprocessing/vietnam_74k.txt', 'r', encoding = 'utf-8')

    dict_74k_processed = []
    for word in file:
        word = word.strip()
        word = word.split()
        word = '_'.join(word)
        dict_74k_processed.append(word)
    
    text_cleaner = vnm_text_cleaner.VNM_TEXT_CLEANER()
    words = text_cleaner.clean_words(corpus)
    words = words.split()
    words = set(words)
    for word in words:
        if word in dict_74k_processed:
            dictionary.append(word)
    return dictionary



url_folder = '/media/hung/Data/NLP/Data/Documents/output/doc'
# corpus = read_file_from_folder(url_folder)
# dictionary = build_dictionnary(corpus)

def folder_file_to_list_document(url_folder):
    files = listdir(url_folder)
    corpus = []
    cnt = 0
    text_cleaner = vnm_text_cleaner.VNM_TEXT_CLEANER()

    for file_name in files:
        file_dir = join(url_folder, file_name)
        f = open(file_dir, 'r')
        words = text_cleaner.clean_words(f.read())
        words = words.split()
        corpus.append(words)
    return corpus

dictionary = '/media/hung/Data/NLP/textrank/dictionary.txt'
def build_vocabulary(dictionary):
    vocab = []
    file = open(dictionary)    
    for word in file:
        vocab.append(word.strip())
    
    word_index = {w: idx for idx, w in enumerate(vocab)}
    return word_index

def cal_tf(corpus, vocab):
    document_counts = len(corpus)
    text_cleaner = vnm_text_cleaner.VNM_TEXT_CLEANER()
    words_tf = dict()

    for doc in corpus:
        words = text_cleaner.clean_words(doc)
        words = words.split()

        for word in words:
            if not word in vocab.keys():
                continue
            
            words_idf[word] = 1
    return words_tf


def cal_idf(corpus, vocab):
    document_counts = len(corpus)
    # text_cleaner = vnm_text_cleaner.VNM_TEXT_CLEANER()
    words_idf = dict()

    for words in corpus:
        # words = text_cleaner.clean_words(doc)
        # words = words.split()
        # words = set(words)

        for word in words:
            if not word in vocab.keys():
                continue
            if not word in words_idf:
                words_idf[word] = 1
            else:
                words_idf[word] += 1
    for word in vocab:
        words_idf[word] = math.log(document_counts / float(1 + words_idf[word]))
    return words_idf

def cal_tf(word, document):
    """
    document: list of word, not a string
    """
    return float(document.count(word)) / len(document)


def cal_tf_idf(word, document, vocab, words_idf):
    """
    document: list of word, not a string
    """
    if not word in vocab.keys():
        return 0.0
    return cal_tf(word, document) * words_idf[word]

word_index = build_vocabulary(dictionary)
corpus = folder_file_to_list_document(url_folder)
words_idf = cal_idf(corpus, word_index)
print(words_idf)

print(cal_tf_idf('vi_phạm', corpus[100], word_index, words_idf))