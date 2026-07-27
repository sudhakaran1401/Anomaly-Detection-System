from anomaly.constants import LABEL_COLUMNS
class DatasetAnalyzer:

    @classmethod
    def analyze(cls, df):

        for column in df.columns:

            if column.lower() in LABEL_COLUMNS:

                return {
                    "dataset_type": "labelled",
                    "target_column": column
                }

        return {
            "dataset_type": "unlabelled",
            "target_column": None
        }