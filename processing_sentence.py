from underthesea import pos_tag


# create sentence in training data
# sample sentence format: [(Word, POS, Tag),...]
class SentenceGetter(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, p, t) for w, p, t in zip(s["Word"].values.tolist(),
                                                           s["POS"].values.tolist(),
                                                           s["Tag"].values.tolist())]
        self.grouped = self.data.groupby("Sentence").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    # get 1 sentence
    def get_next(self):
        s = self.grouped[self.n_sent]
        self.n_sent += 1
        return s

    # get all sentence
    def get_all(self):
        return self.sentences

    def combine_word_with_pos(sent):
        words, pos = zip(*pos_tag(sent))
        sent_n_ = []
        for word in words:
            sent_n_.append(str(word).replace(' ', '_'))
        return (list(zip(sent_n_, pos)))
