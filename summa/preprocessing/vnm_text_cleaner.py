import string
import unicodedata
import logging
import re
import io
from pyvi.pyvi import ViTokenizer as viToken

class VNM_TEXT_CLEANER():
    def __init__(self):
        file = io.open('/media/hung/Data/NLP/textrank/summa/preprocessing/stop_word_list.txt', 'r')
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

    def split_words(self, sentence):
        return viToken.tokenize(sentence)

    def remove_stopwords(self, sentence):
        return " ".join(w for w in sentence.split() if w not in self.stop_word_list)