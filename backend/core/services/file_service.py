import pandas as pd
from pandas.errors import EmptyDataError, ParserError


class FileService:
    MAX_FILE_SIZE = 5 * 1024 * 1024

    @classmethod
    def validate_csv_file(cls, file):

        if not file.name.endswith(".csv"):
            raise ValueError("Only CSV files are allowed.")

        if file.size > cls.MAX_FILE_SIZE:
            raise ValueError("File size must be below 5MB.")

    @staticmethod
    def read_csv_file(file):

        try:
            return pd.read_csv(file)

        except EmptyDataError:
            raise ValueError("CSV file is empty.")

        except ParserError:
            raise ValueError("Invalid CSV format.")
