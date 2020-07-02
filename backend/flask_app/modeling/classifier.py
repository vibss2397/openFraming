"""Classifier related backend functionality."""
import typing as T

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import typing_extensions as TT
from sklearn.metrics import classification_report  # type: ignore
from torch.utils.data.dataset import Dataset
from transformers import AutoConfig  # type: ignore
from transformers import AutoModelForSequenceClassification  # type: ignore
from transformers import AutoTokenizer
from transformers import EvalPrediction  # type: ignore
from transformers import InputFeatures  # type: ignore
from transformers import Trainer
from transformers import TrainingArguments  # type: ignore
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers.trainer_utils import PredictionOutput

from flask_app import utils
from flask_app.modeling.lda import CSV_EXTENSIONS
from flask_app.modeling.lda import EXCEL_EXTENSIONS
from flask_app.modeling.lda import TSV_EXTENSIONS


class ClassificationDataset(Dataset):  # type: ignore
    """Inherits from Torch dataset. Loads and holds tokenized data for a BERT model."""

    def __init__(
        self,
        labels: T.List[str],
        tokenizer: PreTrainedTokenizer,
        label_map: T.Dict[str, int],
        dset_filename: str,
        content_column: str,
        label_column: T.Optional[str],
    ):
        """.

        labels: list of valid labels (can be strings/ints)
        tokenizer: AutoTokenizer object that can tokenize input text
        label_map: maps labels to ints for machine-readability
        dset_filename: name of the filename (full filepath) of the dataset being loaded
        content_column: column name of the content to be read
        label_column: column name where the labels can be found
        """
        suffix = dset_filename.split(".")[-1]
        if suffix in EXCEL_EXTENSIONS:
            doc_reader = pd.read_excel
        elif suffix in CSV_EXTENSIONS:
            doc_reader = pd.read_csv
        elif suffix in TSV_EXTENSIONS:
            doc_reader = lambda b: pd.read_csv(b, sep="\t")
        else:
            raise ValueError(
                f"The file {dset_filename} doesn't have a recognized extension."
            )

        self.labels = labels
        self.label_map = label_map
        self.tokenizer = tokenizer
        df = doc_reader(dset_filename)
        self.len_dset = len(df)

        self.content_series = df[
            content_column
        ]  # For later, if we need to output predictions
        self.encoded_content = self.tokenizer.batch_encode_plus(
            df[content_column], max_length=None, pad_to_max_length=True,
        )
        if label_column is not None:
            self.encoded_labels: T.Optional[T.List[int]] = [
                self.label_map[label] for label in df[label_column]
            ]
        else:
            self.encoded_labels = None
        self.features = []
        for i in range(len(self.encoded_content["input_ids"])):
            inputs = {
                k: self.encoded_content[k][i] for k in self.encoded_content.keys()
            }
            if self.encoded_labels is not None:
                feature = InputFeatures(**inputs, label=self.encoded_labels[i])
            else:
                feature = InputFeatures(**inputs, label=None)
            self.features.append(feature)

    def __len__(self) -> int:
        return self.len_dset

    def __getitem__(self, i: int) -> InputFeatures:
        return self.features[i]

    def get_labels(self) -> T.List[str]:
        return self.labels


ClassificationMetrics = TT.TypedDict(
    "ClassificationMetrics",
    {
        "accuracy": float,
        "macro_f1_score": float,
        "macro_recall": float,
        "macro_precision": float,
    },
)


class ClassifierModel(object):
    """Trainable BERT-based classifier given a training & eval set."""

    def __init__(
        self,
        labels: T.List[str],
        model_path: str,
        train_file: T.Optional[str],
        dev_file: T.Optional[str],
        cache_dir: str,
        output_dir: str,
    ):
        """.

        Args:
            labels: list of valid labels used in the dataset
            model_path: name of model being used or filepath to where the model is stored
            train_file:
            dev_file:
            model_path_tokenizer: name or path of tokenizer being used.
            cache_dir: directory where cache & output are kept.
        """
        assert train_file or dev_file, "Must provide a training or development set."

        self.cache_dir = cache_dir
        self.model_path = model_path
        self.output_dir = output_dir

        self.labels = labels
        self.num_labels = len(labels)
        self.task_name = "classification"

        self.label_map = {label: i for i, label in enumerate(self.labels)}
        self.label_map_reverse = {i: label for i, label in enumerate(self.labels)}

        self.config = AutoConfig.from_pretrained(
            self.model_path,
            num_labels=self.num_labels,
            finetuning_task=self.task_name,
            cache_dir=self.cache_dir,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path, cache_dir=self.cache_dir,
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_path,
            from_tf=False,
            config=self.config,
            cache_dir=self.cache_dir,
        )

        if train_file is not None:
            self.train_dataset = self.make_dataset(
                train_file, utils.CONTENT_COL, utils.LABEL_COL,
            )
        if dev_file is not None:
            self.eval_dataset = self.make_dataset(
                dev_file, utils.CONTENT_COL, utils.LABEL_COL,
            )

    @staticmethod
    def compute_metrics(p: EvalPrediction) -> ClassificationMetrics:
        """
        Compute accuracy of predictions vs labels. Piggy back on sklearn.
        """
        y_true = np.argmax(p.predictions, axis=1)
        y_pred = p.label_ids

        clsf_report_sklearn = classification_report(
            y_true=y_true, y_pred=y_pred, output_dict=True
        )
        final = ClassificationMetrics(
            {
                "accuracy": clsf_report_sklearn["accuracy"],
                "macro_f1_score": clsf_report_sklearn["macro avg"]["f1-score"],
                "macro_recall": clsf_report_sklearn["macro avg"]["recall"],
                "macro_precision": clsf_report_sklearn["macro avg"]["precision"],
            }
        )
        return final

    def make_dataset(
        self, fname: str, content_column: str, label_column: T.Optional[str]
    ) -> ClassificationDataset:
        """Create a Torch dataset object from a file using the built-in tokenizer.

        Inputs:
            fname: name of the file being used
            content_column: column that contains the text we want to analyze
            label_column: column containing the label

        Returns:
            ClassificationDataset object (which is a Torch dataset underneath)
        """
        return ClassificationDataset(
            self.labels,
            self.tokenizer,
            self.label_map,
            fname,
            content_column,
            label_column,
        )

    def train(self) -> None:
        """Train a BERT-based model, using the training set to train & the eval set as
        validation.
        """
        assert self.train_dataset is not None, "train_file was not provided!"

        self.trainer = Trainer(
            model=self.model,
            args=TrainingArguments(
                do_train=True,
                do_eval=True,
                evaluate_during_training=True,
                output_dir=self.output_dir,
            ),
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            compute_metrics=self.compute_metrics,
        )
        self.trainer.train(model_path=self.model_path)
        self.trainer.save_model()
        self.tokenizer.save_pretrained(self.trainer.args.output_dir)

    def train_and_evaluate(self) -> ClassificationMetrics:
        """
        Wrapper on the trainer.evaluate method; evaluate model's performance on eval set
        provided by the user.
        """
        assert self.eval_dataset is not None, "dev_file was not provided!"
        assert self.train_dataset is not None, "train_file was not provided!"

        self.train()
        return self.trainer.evaluate(eval_dataset=self.eval_dataset)

    def predict_and_save_predictions(
        self,
        inference_dset_path: str,
        text_col: str,
        predict_col: str,
        output_file_path: str,
    ) -> None:
        """
        Given a path to a dataset and the column containing text, 
        provide the labels predicted by the model.

        Inputs:
            inference_dset_path: absolute filepath of inference dataset
            text_col: column containing the text we'll analyze
            predict_col: what to name the column with predictions.
            output_file_path: path where the CSV of predictions.

        Outputs:
            list of predictions (as user-supplied labels)
        """
        inference_dset = self.make_dataset(inference_dset_path, text_col, None)
        pred_output: PredictionOutput = self.trainer.predict(inference_dset)
        preds_in_user_labels = [
            inference_dset.labels[i] for i in pred_output.predictions
        ]

        pred_series = pd.Series(preds_in_user_labels, name=predict_col)
        output_df = pd.concat(
            [inference_dset.content_series, pred_series],
            names=[inference_dset.content_series, pred_series.name],
        )

        output_df.to_csv(output_file_path)
