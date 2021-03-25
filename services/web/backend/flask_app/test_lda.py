from settings import Settings
from modeling.lda import Corpus, LDAModeler
corpus = Corpus(
            file_name='test_files/train_fr.csv',
            language='french',
            content_column_name=Settings.CONTENT_COL,
            id_column_name=Settings.ID_COL,
            # phrases_to_join=["anderson cooper", "laura ingraham", "barrack obama"]
        )
print(corpus.df_docs)