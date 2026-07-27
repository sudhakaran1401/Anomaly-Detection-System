from sklearn.svm import OneClassSVM

class SVMDetector:

    @staticmethod
    def train():
        return OneClassSVM(kernel='rbf', gamma='auto')