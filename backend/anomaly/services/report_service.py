import os
import uuid

from django.conf import settings


class ReportService:
    @staticmethod
    def save_result_dataframe(df):

        results_dir = os.path.join(settings.MEDIA_ROOT, "results")

        os.makedirs(results_dir, exist_ok=True)

        file_id = f"{uuid.uuid4()}.csv"

        saved_path = os.path.join(results_dir, file_id)

        df.to_csv(saved_path, index=False)

        return saved_path
