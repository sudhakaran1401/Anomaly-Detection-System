import numpy as np

class EvaluationService:

    @staticmethod
    def evaluate(predictions, scores=None):

        anomaly_count = int( np.sum(predictions == 1) )

        total_records = len(predictions)

        results = {
            "total_records": total_records,
            "anomaly_count": anomaly_count,
            "anomaly_percentage": round( anomaly_count / total_records * 100, 2 )
        }

        if scores is not None:

            results["average_score"] = round( float(np.mean(scores)), 4 )

            results["lowest_score"] = round( float(np.min(scores)), 4 )

        return results