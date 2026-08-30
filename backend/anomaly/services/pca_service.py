from sklearn.decomposition import PCA
import numpy as np

class PCAService:

    @staticmethod
    def reduce(data):

        rows, cols = data.shape

        if rows < 2 or cols < 2:

            result = np.zeros((rows, 2))

            if cols >= 1:
                result[:, 0] = data[:, 0]

            return result

        pca = PCA(n_components=2)

        return pca.fit_transform(data)
