class FeatureEngineeringService:

    @staticmethod
    def generate_features(df):

        df = df.copy()

        numeric_cols = df.select_dtypes(include=["number"]).columns

        TARGET_COLUMNS = {
            "label",
            "target",
            "class",
            "anomaly",
            "is_anomaly",
            "fraud",
            "is_fraud"
        }

        # Avoid feature explosion
        if len(numeric_cols) <= 20:

            for col in numeric_cols:
                if col.lower() in TARGET_COLUMNS:
                     continue

                mean = df[col].mean()
                std = df[col].std()

                if std and std > 0:
                    df[f"{col}_zscore"] = ( (df[col] - mean) / std )
                    
        if ( "cpu_usage" in df.columns and "memory_usage" in df.columns ):

            df["cpu_memory_ratio"] = (
                df["cpu_usage"] /
                (df["memory_usage"] + 1)
            )

        if ( "response_time_ms" in df.columns and "cpu_usage" in df.columns ):
            
            df["response_per_cpu"] = (
                df["response_time_ms"] /
                (df["cpu_usage"] + 1)
            )

        return df
