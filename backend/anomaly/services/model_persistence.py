import os
import uuid
import joblib

class ModelPersistenceService:

    BASE_DIR = "saved_models"

    @classmethod
    def save_model(cls, model, model_name, dataset_name):

        os.makedirs(cls.BASE_DIR, exist_ok=True)

        unique_id = uuid.uuid4().hex[:8]

        filename = ( f"{dataset_name}_{model_name}_{unique_id}.pkl" )

        path = os.path.join(cls.BASE_DIR, filename)

        joblib.dump(model, path)

        return path

    @classmethod
    def load_model(cls, path):

        return joblib.load(path)
