from sklearn.neighbors import LocalOutlierFactor

class LOFDetector:

    @staticmethod
    def train(contamination=0.05):
        return LocalOutlierFactor( contamination=contamination, novelty=True )