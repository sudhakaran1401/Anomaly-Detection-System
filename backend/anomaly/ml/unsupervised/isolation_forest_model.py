from sklearn.ensemble import IsolationForest

class IsolationForestDetector:

    @staticmethod
    def train(contamination=0.05):
        return IsolationForest( contamination=contamination, random_state=42, n_estimators=100 )