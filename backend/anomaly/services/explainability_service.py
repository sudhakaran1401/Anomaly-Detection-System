class ExplainabilityService:

    ANOMALY_THRESHOLD = 2

    @staticmethod
    def explain_row( row, numeric_columns, column_stats ):
        
        unusual_columns = []

        for column in numeric_columns:

            mean = column_stats[column]["mean"]
            std = column_stats[column]["std"]

            if std and std > 0:

                deviation = abs( row[column] - mean ) / std

                if deviation > ExplainabilityService.ANOMALY_THRESHOLD:
                    unusual_columns.append(column)

        if row.get("result") != "Anomaly":
            return "Within normal range"

        if len(unusual_columns) == 1:
            return ( f"{unusual_columns[0]} " "deviates significantly from normal behaviour" )

        if len(unusual_columns) > 1:
            return ( "Anomaly influenced by: " + ", ".join(unusual_columns[:5]) )

        return "Detected by anomaly detection model"

    @staticmethod
    def generate_explanations( df, numeric_columns, column_stats ):

        return df.apply(
            lambda row: ExplainabilityService.explain_row( row, numeric_columns, column_stats ),
            axis=1,
        )