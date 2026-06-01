
import numpy as np

class WeightedEnsembleDetector:

    def __init__(self, models, weights=None, threshold=0.5):

        self.models = models

        if weights is None:
            weights = [1 / len(models)] * len(models)

        self.weights = weights
        self.threshold = threshold

    def fit(self, X):

        for model in self.models:

            if hasattr(model, "fit"):
                model.fit(X)

    def predict(self, X):

        predictions = []

        for model in self.models:

            pred = model.predict(X)

            pred = np.where(pred == -1, 1, 0)

            predictions.append(pred)

        weighted_scores = np.zeros(len(X))

        for pred, weight in zip(predictions, self.weights):
            weighted_scores += pred * weight

        final_predictions = np.where( weighted_scores >= self.threshold, 1, 0 )

        return final_predictions

    def confidence_scores(self, X):

        predictions = []

        for model in self.models:

            pred = model.predict(X)
            pred = np.where(pred == -1, 1, 0)

            predictions.append(pred)

        weighted_scores = np.zeros(len(X))

        for pred, weight in zip(predictions, self.weights):
            weighted_scores += pred * weight

        return weighted_scores
