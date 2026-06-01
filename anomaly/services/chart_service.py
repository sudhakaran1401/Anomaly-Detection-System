from django.conf import settings
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import uuid

class ChartService:

    @staticmethod
    def _generate_chart_path(prefix):

        return os.path.join( settings.MEDIA_ROOT, f"{prefix}_{uuid.uuid4().hex}.png" )
    
    @staticmethod
    def generate_scatter_data(df, numeric_columns):

        scatter_data = []

        if len(numeric_columns) < 2:
            return scatter_data

        x_col = numeric_columns[0]
        y_col = numeric_columns[1]

        for _, row in df.iterrows():
            scatter_data.append(
                {"x": row[x_col], "y": row[y_col], "label": row.get("result", "Normal")}
            )

        return scatter_data

    @staticmethod
    def generate_summary_chart( normal, anomalies ):

        labels = [ 'Normal', 'Anomalies' ]

        values = [ normal, anomalies ]

        plt.title( "Bar Anomaly Visualization" )

        plt.figure(figsize=(5, 4))

        plt.bar( labels, values )

        chart_path = ChartService._generate_chart_path( "chart_summary" )

        plt.savefig(chart_path)

        plt.close()

        return chart_path

    @staticmethod
    def generate_pca_pdf_chart(df):

        plt.figure(figsize=(6, 5))

        normal_data = df[ df["result"] == "Normal" ]

        anomaly_data = df[ df["result"] == "Anomaly" ]

        # NORMAL POINTS
        plt.scatter( normal_data["pca_x"], normal_data["pca_y"], label="Normal", alpha=0.7 )

        # ANOMALY POINTS
        plt.scatter( anomaly_data["pca_x"], anomaly_data["pca_y"], label="Anomaly", alpha=0.9 )

        plt.title( "PCA Anomaly Visualization" )

        plt.xlabel("PCA X")

        plt.ylabel("PCA Y")

        plt.legend()

        chart_path = ChartService._generate_chart_path( "pca_chart" )

        plt.savefig(chart_path)

        plt.close()

        return chart_path
    
    @staticmethod
    def generate_histogram_chart(df):

        plt.figure(figsize=(6, 4))

        scores = df[ "anomaly_score" ].fillna(0)

        plt.hist( scores, bins=20 )

        plt.title( "Anomaly Score Distribution" )

        plt.xlabel( "Anomaly Score" )

        plt.ylabel( "Frequency" )

        chart_path = ChartService._generate_chart_path( "histogram_chart" )

        plt.savefig(chart_path)

        plt.close()

        return chart_path
    
    @staticmethod
    def generate_confusion_matrix(confusion_matrix):

        plt.figure(figsize=(5, 4))

        plt.imshow( confusion_matrix, interpolation="nearest" )

        plt.title("Confusion Matrix")

        plt.colorbar()

        labels = ["0", "1"]

        plt.xticks( np.arange(len(labels)), labels )

        plt.yticks( np.arange(len(labels)), labels )

        plt.xlabel("Predicted Label")

        plt.ylabel("True Label")

        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix[0])):

                plt.text(
                    j,
                    i,
                    str(confusion_matrix[i][j]),
                    ha="center",
                    va="center"
                )

        chart_path = os.path.join( settings.MEDIA_ROOT, f"confusion_matrix_{uuid.uuid4().hex}.png"
)

        plt.savefig(chart_path)

        plt.close()

        return chart_path
