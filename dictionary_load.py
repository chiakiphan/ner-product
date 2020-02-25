import io
import pandas as pd
import pickle


class DictionaryLoader:
    def __init__(self):
        self.words_data = None

    def read_txt(self, path):
        with io.open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return text

    def read_bin(self, path):
        with open(path, 'rb') as fr:
            model = pickle.load(fr)
        return model

    def read_csv(self, path):
        data = pd.read_csv(path, encoding='utf8', error_bad_lines=False, header=None,
                           names=["Word", "POS", "Tag", "Sentence"],
                           sep=' ')
        data = data.fillna(method="ffill")
        return data

    def save_model(self, path, model):
        with open(path, 'wb+') as fw:
            pickle.dump(model, fw)

    @property
    def words(self):
        if not self.words_data:
            content = DictionaryLoader.read_csv(self.data_file)
            # words = content.split("\n")
            self.words_data = content
        return self.words_data
