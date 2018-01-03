import string
import unicodedata
import logging
import re
import io
from pyvi.pyvi import ViTokenizer as viToken
from pyvi.pyvi import ViPosTagger as viPosTag
from summa.syntactic_unit import SyntacticUnit
import re


def to_unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, str):
        return text
    return unicode(text, encoding, errors=errors)

eos = ['E']
punc = string.punctuation
punc = punc.replace('_', '')
punc = punc.replace('/', '')
RE_PUNCT = re.compile('([%s])+' % re.escape(punc), re.UNICODE)
def strip_punctuation(s):
    s = to_unicode(s)
    return RE_PUNCT.sub("", s)


order_list = [ch + ')' for ch in string.ascii_lowercase]

class VNM_TEXT_CLEANER():
    def __init__(self):
        file = io.open('/media/hung/Data/NLP/textrank/summa/preprocessing/stop_word_list.txt', 'r', encoding = 'utf-8')
        self.stop_word_list = file.read()
        
    def split_sentences(self, text):
        text = re.sub(r'--+', '', text)
        text = re.sub(r'  +', ' ', text)

        RE_SENTENCE = re.compile('(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)')
        
        def get_sentences(text):
            for match in RE_SENTENCE.finditer(text):
                yield match.group()

        draft_sentences = list(get_sentences(text))
        sentences = []
        # print('ORDER LIST', order_list)
        for sent in draft_sentences:
            # print('Sent', sent)
            sent = sent.strip()

            if len(sentences) == 0:
                sentences.append(sent)                

            if len(sentences) > 0 and sentences[-1][-1] in punc:
                sentences.append(sent)
                continue
            
            token = viToken.tokenize(sentences[-1])
            pos = viPosTag.postagging(token)

            print('SENT', sent)
            print(pos[0][-1], pos[1][-1])
            if (sent[0].isupper() or sent[0].isdigit() or sent[:2] in order_list or sent[0] in punc):
                    # and (pos[1][-1] in eos):
                sentences.append(sent)
            else:
                sentences[-1] += ' ' + sent
                
        return sentences

    def clean_words(self, sentence):
        def split_words(sentence):
            return viToken.tokenize(sentence)

        def remove_stopwords(s):
            return "" if s in self.stop_word_list else s
        
        sentence = sentence.lower()
        sentence = strip_punctuation(sentence)
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
    # text = text.replace('\n', ' ')

    text_cleaner = VNM_TEXT_CLEANER()
    original_sentences = text_cleaner.split_sentences(text)
    filtered_sentences = [text_cleaner.clean_words(sentence) for sentence in original_sentences]
    return text_cleaner.merge_syntactic_units(original_sentences, filtered_sentences)
