class AnalyticsService:
    @staticmethod
    def generate_column_stats(df, numeric_columns):

        return {
            col: {
                "mean": df[col].mean(),
                "std": df[col].std()
            }
            for col in numeric_columns
        }

    @staticmethod
    def explain_anomaly(row, numeric_columns, column_stats):

        unusual_cols = []

        for col in numeric_columns:

            mean = column_stats[col]["mean"]
            std = column_stats[col]["std"]

            if std and std > 0:

                deviation = abs(row[col] - mean) / std

                ANOMALY_DEVIATION_THRESHOLD = 2

                # Professional threshold
                if deviation > ANOMALY_DEVIATION_THRESHOLD:
                    unusual_cols.append(col)

        if row.get("result") == "Anomaly":

            if len(unusual_cols) == 1:
                return f"{unusual_cols[0]} deviates significantly from normal behaviour"

            if len(unusual_cols) > 1:
                return f"Anomaly influenced by: {', '.join(unusual_cols[:5])}"

            return "Detected by anomaly detection model"

        return "Within normal range"
