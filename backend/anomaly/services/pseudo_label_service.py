class PseudoLabelService:

    @staticmethod
    def generate(result_df):

        df = result_df.copy()

        if "result" not in df.columns:
            raise ValueError("Result column not found.")

        # Generate binary label
        df["label"] = (
            df["result"]
              .map({
                  "Normal": 0,
                  "Anomaly": 1
              })
              .astype(int)
        )
        
        df.drop(
            columns=[
                "result",
                "reason"
            ],
            inplace=True,
            errors="ignore"
        )

        return df