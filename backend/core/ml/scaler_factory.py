from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler 

class ScalerFactory:

    @staticmethod
    def get_scaler(scaler_type):

        scalers = {

            "standard": StandardScaler(),

            "minmax": MinMaxScaler(),

            "robust": RobustScaler()
        }

        return scalers.get( scaler_type, StandardScaler() )