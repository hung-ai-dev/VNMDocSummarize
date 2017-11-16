import string
import unicodedata
import logging
import re
import io
from pyvi.pyvi import ViTokenizer as viToken

class VNM_TEXT_CLEANER():
    def __init__(self):
        file = io.open('/media/hung/Data/NLP/textrank/summa/preprocessing/stop_word_list.txt', 'r', encoding = 'utf-8')
        self.stop_word_list = file.read()
        
    def split_sentences(self, text):
        SEPARATOR = r"@"
        RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')
        UNDO_AB_SENIOR = re.compile("([A-Z][a-z]{1,2}\.)" + SEPARATOR + "(\w)")
        UNDO_AB_ACRONYM = re.compile("(\.[a-zA-Z]\.)" + SEPARATOR + "(\w)")

        def undo_replacement(sentence):
            return replace_with_separator(sentence, r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM])

        def replace_with_separator(text, separator, regexs):
            replacement = r"\1" + separator + r"\2"
            result = text
            for regex in regexs:
                result = regex.sub(replacement, result)
            return result

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
                        for w in words.split() if w not in self.stop_word_list)