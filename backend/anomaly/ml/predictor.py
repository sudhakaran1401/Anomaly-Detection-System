import numpy as np
from sklearn.cluster import DBSCAN
from anomaly.services.model_persistence import ( ModelPersistenceService )

class Predictor:

    @staticmethod
    def run(model, X):

        if isinstance(model, DBSCAN):

            model.fit(X)

            predictions = model.labels_

            predictions = np.where( predictions == -1, -1, 1 )

            return predictions

        model.fit(X)

        return model.predict(X)
    
    @staticmethod
    def save_and_predict(model, X, model_name, dataset_name):
        
        model.fit(X)

        if isinstance(model, DBSCAN):

            predictions = np.where( model.labels_ == -1, -1, 1 )

        else:

            predictions = model.predict(X)

        model_path = ModelPersistenceService.save_model( model, model_name, dataset_name )

        return predictions, model_path