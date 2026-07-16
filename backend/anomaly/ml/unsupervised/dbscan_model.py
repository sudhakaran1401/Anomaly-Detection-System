from sklearn.cluster import DBSCAN

class DBSCANDetector:

    @staticmethod
    def train():
        return DBSCAN(eps=0.5, min_samples=5)