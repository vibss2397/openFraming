from settings import Settings
from modeling.lda import Corpus, LDAModeler


class TestLDA:
    def __init__(self):
        corpus = Corpus(
                    file_name='test_files/train_fr.csv',
                    language='english',
                    content_column_name=Settings.CONTENT_COL,
                    id_column_name=Settings.ID_COL,
                    # phrases_to_join=["anderson cooper", "laura ingraham", "barrack obama"]
                )
        lda = LDAModeler(
                    corpus,
                    iterations=100,
                    mallet_bin_directory= "c:/mallet/mallet-2.0.8/bin",
                )
    def get_processed_dataset(self):
        return self.df_docs
    def run topic_modelling:
        a = lda.model_topics()
        return a