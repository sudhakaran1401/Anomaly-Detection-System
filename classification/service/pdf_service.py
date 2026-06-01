
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image 

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib import colors

class PDFService:

    @staticmethod
    def generate_classification_pdf(report):

        response = HttpResponse( content_type="application/pdf" )

        response[ "Content-Disposition" ] = ( 'attachment; filename="classification_report.pdf"' )

        doc = SimpleDocTemplate(response)

        styles = getSampleStyleSheet()

        elements = []

        metrics = report["metrics"]

        summary = metrics["summary"]

        dataset_summary = metrics.get( "dataset_summary", {} )

        print("dataset_summary =", dataset_summary)

        cm = metrics["confusion_matrix"]

        TN = cm[0][0]
        FP = cm[0][1]
        FN = cm[1][0]
        TP = cm[1][1]

        # ==================================================
        # TITLE
        # ==================================================

        elements.append( Paragraph( "Classification Analysis Report", styles["Title"] ) )

        elements.append( Spacer(1, 20) )

        # ==================================================
        # DATASET INFORMATION
        # ==================================================

        elements.append( Paragraph( "Dataset Information", styles["Heading2"] ) )

        dataset_table = Table(
            [
                ["Attribute", "Value"],

                ["Dataset Name", report["filename"]],

                ["Model", report["model_name"]]
            ],
            colWidths=[140, 260]
        )

        dataset_table.setStyle(
            TableStyle([
                ("BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey),

                ("GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black),

                ("FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold")
            ])
        )

        elements.append(dataset_table)

        elements.append( Spacer(1, 15) )

        # ==================================================
        # DATASET STATISTICS
        # ==================================================

        if dataset_summary:

            elements.append( Paragraph( "Dataset Statistics", styles["Heading2"] ) )

            stats_table = Table(
                [
                    ["Metric", "Value"],

                    ["Total Dataset Records", dataset_summary.get( "total_dataset_records", "-" )],

                    ["Training Records", dataset_summary.get( "training_records", "-" )],

                    ["Testing Records", dataset_summary.get( "testing_records", "-" )]
                ],
                colWidths=[250, 120]
            )

            stats_table.setStyle(
                TableStyle([
                    ("BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey),

                    ("GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black),

                    ("FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold")
                ])
            )

            elements.append(stats_table)

            elements.append( Spacer(1, 15) )

        # ==================================================
        # DETECTION SUMMARY
        # ==================================================

        elements.append( Paragraph( "Detection Summary", styles["Heading2"] ) )

        detection_table = Table(
            [
                ["Metric", "Value"],

                ["Detected Anomalies",
                summary["detected_anomalies"]],

                ["Missed Anomalies",
                summary["missed_anomalies"]],

                ["False Alarms",
                summary["false_alarms"]]
            ],
            colWidths=[250, 120]
        )

        detection_table.setStyle(
            TableStyle([
                ("BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey),

                ("GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black),

                ("FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold")
            ])
        )

        elements.append(detection_table)

        elements.append( Spacer(1, 15) )

        # ==================================================
        # MODEL PERFORMANCE
        # ==================================================

        elements.append( Paragraph( "Model Performance", styles["Heading2"] ) )

        performance_table = Table(
            [
                ["Metric", "Value"],

                ["Accuracy",
                f"{metrics['accuracy']*100:.2f}%"],

                ["Precision",
                f"{metrics['precision']*100:.2f}%"],

                ["Recall",
                f"{metrics['recall']*100:.2f}%"],

                ["F1 Score",
                f"{metrics['f1']*100:.2f}%"],

                ["ROC-AUC",
                f"{metrics['roc_auc']*100:.2f}%"]
            ],
            colWidths=[250, 120]
        )

        performance_table.setStyle(
            TableStyle([
                ("BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey),

                ("GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black),

                ("FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold")
            ])
        )

        elements.append(performance_table)

        elements.append(
            Spacer(1, 15)
        )

        # ==================================================
        # CONFUSION MATRIX TABLE
        # ==================================================

        elements.append( Paragraph( "Confusion Matrix", styles["Heading2"] ) )

        cm_table = Table(
            [
                ["Actual / Predicted",
                "Predicted Normal",
                "Predicted Anomaly"],

                ["Actual Normal",
                TN,
                FP],

                ["Actual Anomaly",
                FN,
                TP]
            ],
            colWidths=[150, 100, 100]
        )

        cm_table.setStyle(
            TableStyle([
                ("BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey),

                ("GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black),

                ("FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold")
            ])
        )

        elements.append(cm_table)

        elements.append( Spacer(1, 20) )

        # ==================================================
        # CONFUSION MATRIX IMAGE
        # ==================================================

        try:

            chart_path = report.get( "confusion_matrix_chart" )

            if chart_path:

                elements.append( Image( chart_path, width=320, height=240 ) )

                elements.append( Spacer(1, 20) )

        except Exception:
            pass

        # ==================================================
        # PERFORMANCE INSIGHT
        # ==================================================

        elements.append( Paragraph( "Performance Insight", styles["Heading2"] ) )

        insight = (
            f"The model detected {TP} anomalies and "
            f"missed {FN}. "
            f"False alarms recorded: {FP}. "
            f"Overall accuracy achieved: "
            f"{metrics['accuracy']*100:.2f}%."
        )

        elements.append( Paragraph( insight, styles["BodyText"] ) )

        doc.build(elements)

        return response