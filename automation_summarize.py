from pyvi.pyvi import ViTokenizer as vnToken
import summa.summarizer as summarizer
import summa.keywords as keywords
from summa.export import gexf_export
from summa.preprocessing import vnm_text_cleaner
import io
import sys
from nltk import sent_tokenize
import re
import glob

if __name__ == '__main__':
    documents = glob.glob('/media/hung/Data/NLP/Data/TextDocuments/*')

    for doc in documents:
        inp = io.open(doc, 'r', encoding = 'utf-8')
        doc_id = doc.split('/')[-1].split('.')[0]
        text = inp.read()
        sum = summarizer.summarize(text, ratio=0.2, number_of_sentences = 1)
        inp.close()

        out = io.open(doc_id + '.txt', 'w', encoding = 'utf-8')
        out.write(sum)
        out.close()