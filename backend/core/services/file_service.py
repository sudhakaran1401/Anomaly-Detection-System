import os

import pandas as pd
from pandas.errors import EmptyDataError, ParserError


class FileService:
    MAX_FILE_SIZE = 5 * 1024 * 1024
    ALLOWED_EXTENSION = ".csv"

    @classmethod
    def validate_csv_file(cls, file):
        filename = getattr(file, "name", "") or ""
        safe_name = os.path.basename(str(filename))

        if not filename.lower().endswith(cls.ALLOWED_EXTENSION):
            raise ValueError("Only CSV files are allowed.")

        if safe_name != str(filename).replace("\\", "/").split("/")[-1]:
            raise ValueError("Invalid filename.")

        if safe_name in {"", ".", ".."} or any(ord(ch) < 32 for ch in safe_name):
            raise ValueError("Invalid filename.")

        if getattr(file, "size", 0) > cls.MAX_FILE_SIZE:
            raise ValueError("File size must be below 5MB.")

        # Validate the supplied filename itself; never trust MIME type as the
        # security boundary because clients can forge Content-Type.
        content_type = getattr(file, "content_type", "") or ""
        if content_type and content_type not in {
            "text/csv",
            "application/csv",
            "text/plain",
            "application/vnd.ms-excel",
        }:
            raise ValueError("Unsupported file content type.")

    @staticmethod
    def read_csv_file(file):
        try:
            if hasattr(file, "seek"):
                file.seek(0)

            # Read the raw header first so pandas cannot rename duplicates.
            raw = file.read()

            if isinstance(raw, str):
                raw = raw.encode("utf-8")

            if not raw:
                raise ValueError("CSV file is empty.")

            text = raw.decode("utf-8")

            first_line = text.splitlines()[0] if text.splitlines() else ""
            columns = [column.strip() for column in first_line.split(",")]

            if not columns:
                raise ValueError("CSV file contains no columns.")

            if any(not column for column in columns):
                raise ValueError("CSV file contains an empty column name.")

            if len(set(columns)) != len(columns):
                raise ValueError("CSV file contains duplicate column names.")

            if hasattr(file, "seek"):
                file.seek(0)

            df = pd.read_csv(file)

        except EmptyDataError as exc:
            raise ValueError("CSV file is empty.") from exc
        except ParserError as exc:
            raise ValueError("Invalid CSV format.") from exc
        except UnicodeDecodeError as exc:
            raise ValueError("CSV file must use UTF-8 encoding.") from exc
        finally:
            if hasattr(file, "seek"):
                file.seek(0)

        if df.empty:
            raise ValueError("CSV file contains no data rows.")

        if len(df.columns) == 0:
            raise ValueError("CSV file contains no columns.")

        if any(
            str(column).strip() == ""
            or str(column).strip().startswith("Unnamed:")
            for column in df.columns
        ):
            raise ValueError("CSV file contains an empty column name.")

        return df