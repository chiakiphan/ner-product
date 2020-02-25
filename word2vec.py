from dictionary_load import DictionaryLoader
import re
from underthesea import pos_tag


words = DictionaryLoader("/home/citigo/Downloads/1M_san_pham_my_pham.csv").words
lower_words = set([word.lower() for word in words])


def word2features(sent, position):
    word = sent[position][0]
    postag = sent[position][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isalpha()': multi_word(word),
        'word.digitand_comma()': digitand_comma(word),
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.hasdigit()': check_digit(word),
        'postag': postag,
        'word.isstopword()': check_stopword(word),
        'number_syllable': count_syllable(word),
    }
    if position > 0:
        word1 = sent[position - 1][0]
        word2 = word1+' '+word
        if position < len(sent)-1:
            word3 = word2+sent[position + 1][0]
        else:
            word3 = word2
        postag1 = sent[position - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word1.lower()': word2.lower(),
            '-1:word2.lower()': word3.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isalpha()': multi_word(word1),
            '-1:word.isbidict()': text_is_in_dict(word2),
            '-1:word.istridict()': text_is_in_dict(word3),
            '-1:word.digitand_comma()': digitand_comma(word1),
            '-1:word.isupper()': word1.isupper(),
            '-1:word.isstopword()': check_stopword(word1),
            '-1:word.hasdigit()': check_digit(word1),
            '-1:postag': postag1,
            '-1:number_syllable': count_syllable(word1),
            # '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if position < len(sent)-1:
        word1 = sent[position + 1][0]
        word2 = word + ' ' + word1
        if position > 0:
            word3 = sent[position - 1][0] + word2
        else:
            word3 = word2
        postag1 = sent[position + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word1.lower()': word2.lower(),
            '+1:word2.lower()': word3.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.digitand_comma()': digitand_comma(word1),
            '+1:word.isdict()': text_is_in_dict(word2),
            '+1:word.istridict()': text_is_in_dict(word3),
            '+1:word.isalpha()': multi_word(word1),
            '+1:word.isupper()': word1.isupper(),
            '+1:word.hasdigit()': check_digit(word1),
            '+1:word.isstopword()': check_stopword(word1),
            '+1:postag': postag1,
            '+1:number_syllable': count_syllable(word),
            # '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def check_stopword(word):

    return True


def check_digit(word):
    for c in word:
        if str(c).isdigit():
            return True
    return False


def digitand_comma(word):
    if '.' in word or ',' in word:
        return True
    return False


def count_syllable(word):
    return len(str(word).split('_'))


def multi_word(word):
    if ' ' in word:
        return True
    return False


def text_is_in_dict(word):
    for words in lower_words:
        if str(word).lower() in str(words).lower():
            return True
    return False
