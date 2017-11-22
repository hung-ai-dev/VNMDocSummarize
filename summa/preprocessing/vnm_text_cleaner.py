import string
import unicodedata
import logging
import re
import io
from pyvi.pyvi import ViTokenizer as viToken
from summa.syntactic_unit import SyntacticUnit

class VNM_TEXT_CLEANER():
    def __init__(self):
        file = io.open('/media/hung/Data/NLP/textrank/summa/preprocessing/stop_word_list.txt', 'r', encoding = 'utf-8')
        self.stop_word_list = file.read()
        
    def split_sentences(self, text):
        RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')
        
        def get_sentences(text):
            for match in RE_SENTENCE.finditer(text):
                yield match.group()

        return list(get_sentences(text))

    def clean_words(self, sentence):
        def to_unicode(text, encoding='utf8', errors='strict'):
            """Convert a string (bytestring in `encoding` or unicode), to unicode."""
            if isinstance(text, str):
                return text
            return unicode(text, encoding, errors=errors)
        sentence = sentence.lower()
        punc = string.punctuation
        punc = punc.replace('_', '')
        RE_PUNCT = re.compile('([%s])+' % re.escape(punc), re.UNICODE)
        def strip_punctuation(s):
            s = to_unicode(s)
            return RE_PUNCT.sub("", s)

        def split_words(sentence):
            return viToken.tokenize(sentence)

        def remove_stopwords(s):
            return "" if s in self.stop_word_list else s
        
        words = split_words(sentence)
        return " ".join(strip_punctuation(remove_stopwords(w)) \
                        for w in words.split() if w not in self.stop_word_list).strip()
    
    def merge_syntactic_units(self, original_units, filtered_units, tags=None):
        units = []
        for i in range(len(original_units)):
            if filtered_units[i] == '':
                continue

            text = original_units[i]
            token = filtered_units[i]
            tag = tags[i][1] if tags else None
            sentence = SyntacticUnit(text, token, tag)
            sentence.index = i

            units.append(sentence)

        return units


def _clean_text_by_sentences(text, language):
    text_cleaner = VNM_TEXT_CLEANER()
    original_sentences = text_cleaner.split_sentences(text)
    filtered_sentences = [text_cleaner.clean_words(sentence) for sentence in original_sentences]
    return text_cleaner.merge_syntactic_units(original_sentences, filtered_sentences)