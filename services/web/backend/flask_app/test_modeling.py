from settings import Settings
from modeling.lda import Corpus, LDAModeler


class TestLDA:
    def __init__(self):
        self.corpus = Corpus(
                    file_name='test_files/train.csv',
                    language='english',
                    content_column_name=Settings.CONTENT_COL,
                    id_column_name=Settings.ID_COL,
                    phrases_to_join=["anderson cooper", "laura ingraham", "barrack obama"]
                )
        self.lda = LDAModeler(
                    self.corpus,
                    iterations=100,
                    mallet_bin_directory= "c:/mallet/mallet-2.0.8/bin",
                )
    def get_processed_dataset(self):
        return self.corpus.df_docs
    def run_topic_modelling(self):
        a = lda.model_topics()
        return a

lda_in = TestLDA()
print(lda_in.get_processed_dataset())