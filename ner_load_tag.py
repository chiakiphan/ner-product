import word2vec as w2
from dictionary_load import DictionaryLoader
from processing_sentence import SentenceGetter
from underthesea import word_tokenize
from utils import tokenize


class Tagger:
    def __init__(self):
        self.tagger = None
        self.path_to_model = 'ner.crfsuite'
        self.process_file = DictionaryLoader()

    # return list tuple include word and label.
    # mode 'text' is used to convert sentence to normal sentence,
    # where the words are the product to be capitalized.
    def combine_tag_with_word(self, tags, sent, mode=None):
        words = word_tokenize(sent)
        f_sent_dict = (list(zip(words, tags)))
        if mode is 'text':
            f_sent_text = ''
            for word in f_sent_dict:
                w = word[0].lower()
                t = word[1]
                if t is not 'O':
                    w = w.upper()
                f_sent_text += w + ' '
            return f_sent_text.rstrip(' ')
        return f_sent_dict

    def ner(self, text, mode=None):
        if self.tagger is None:
            self.tagger = self.process_file.read_bin(self.path_to_model)
        test_features = w2.sent2features(SentenceGetter.combine_word_with_pos(tokenize(text)))
        prediction = self.tagger.predict([test_features])[0]
        return Tagger().combine_tag_with_word(prediction, text, mode)


def test():
    ner_tag = Tagger()
    sent = 'dầu gội Thái Dương 3 dùng có tốt k'
    print(ner_tag.ner(sent, mode='text'))
    print(ner_tag.ner(sent))


if __name__ == '__main__':
    test()
