from pyvi.pyvi import ViTokenizer as vnToken
import summa.summarizer as summarizer
import summa.keywords as keywords
from summa.export import gexf_export
import io
import sys

from summa.preprocessing import vnm_text_cleaner

f = io.open('document.txt', 'r', encoding = 'utf-8')
text = f.read()
text_cleaner = vnm_text_cleaner.VNM_TEXT_CLEANER()
print(text)
print('-------------')
sentences = text_cleaner.split_sentences(text)
cnt = 1
for sentence in sentences:
    print('Sentence: ', cnt)
    print(sentence)
    sentence = text_cleaner.clean_words(sentence)
    print(sentence)
    cnt += 1
print('----------------------')
print(summarizer.summarize(text, ratio=0.2))
print('----------------------')