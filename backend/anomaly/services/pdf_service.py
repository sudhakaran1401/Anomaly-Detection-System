import os
from datetime import datetime

import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from anomaly.services.chart_service import ChartService


class PdfService:

    @staticmethod
    def generate_anomaly_pdf(request, metadata):

        file_path = request.session.get("result_file")

        if not file_path or not os.path.exists(file_path):
            return HttpResponse("No data found", status=404)

        df = pd.read_csv(file_path)

        data = PdfService._apply_filter( df.to_dict(orient="records"), request.GET.get("filter"), )

        summary = PdfService._build_summary(data)

        return PdfService._build_pdf_response( df=df, summary=summary, metadata=metadata, )

    @staticmethod
    def _apply_filter(data, filter_type):

        if filter_type == "normal":
            return [
                row
                for row in data
                if row.get("result") == "Normal"
            ]

        if filter_type == "anomaly":
            return [
                row
                for row in data
                if row.get("result") == "Anomaly"
            ]

        return data

    @staticmethod
    def _build_summary(data):

        total = len(data)

        anomalies = len([
            row
            for row in data
            if row.get("result") == "Anomaly"
        ])

        normal = total - anomalies

        anomaly_percentage = ( round((anomalies / total) * 100, 2) if total else 0 )

        return {
            "total": total,
            "anomalies": anomalies,
            "normal": normal,
            "anomaly_percentage": anomaly_percentage,
        }

    @staticmethod
    def _build_pdf_response(df, summary, metadata):

        response = HttpResponse( content_type="application/pdf" )

        response["Content-Disposition"] = ( 'attachment; filename="report.pdf"' )

        doc = SimpleDocTemplate(response)

        styles = getSampleStyleSheet()

        content = []

        content.append( Paragraph( "Smart Anomaly Detection Report", styles["Title"], ) )

        content.append(Spacer(1, 16))

        generated_time = datetime.now().strftime( "%B %d, %Y %I:%M %p" )

        content.append( Paragraph( f"<b>Generated:</b> {generated_time}", styles["Normal"], ) )

        content.append(Spacer(1, 8))

        content.append( Paragraph( f"<b>Dataset:</b> {metadata['uploaded_filename']}", styles["Normal"], ) )

        content.append(Spacer(1, 8))

        content.append( Paragraph( f"<b>Model:</b> {metadata['model_name']}", styles["Normal"], ) )

        content.append(Spacer(1, 8))

        content.append( Paragraph( f"<b>Scaler:</b> {metadata['scaler_type']}", styles["Normal"], ) )

        content.append(Spacer(1, 8))

        content.append( Paragraph( f"<b>Contamination:</b> {metadata['contamination']}", styles["Normal"], ) )

        content.append(Spacer(1, 12))

        content.append( Paragraph( "<b>Detection Summary</b>", styles["Heading2"], ) )

        content.append(Spacer(1, 8))

        summary_data = [
            ["Metric", "Value"],
            ["Total Records", summary["total"]],
            ["Normal Records", summary["normal"]],
            ["Anomalies Detected", summary["anomalies"]],
            [
                "Anomaly Percentage",
                f"{summary['anomaly_percentage']}%",
            ],
        ]

        summary_table = Table( summary_data, colWidths=[220, 150], )

        summary_table.setStyle(
            TableStyle(
                [
                    ( "BACKGROUND", (0, 0), (-1, 0), colors.darkblue, ),

                    ( "TEXTCOLOR", (0, 0), (-1, 0), colors.white, ),

                    ( "FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold", ),

                    ( "BOTTOMPADDING", (0, 0), (-1, 0), 12, ),

                    ( "BACKGROUND", (0, 1), (-1, -1), colors.beige, ),

                    ( "GRID", (0, 0), (-1, -1), 1, colors.black, ),

                    ( "ALIGN", (0, 0), (-1, -1), "CENTER", ),
                ]
            )
        )

        content.append(summary_table)

        content.append(Spacer(1, 18))

        insight = (
            f"{summary['anomalies']} anomalies were detected "
            f"out of {summary['total']} records. "
            f"The dataset appears "
        )

        if summary["anomaly_percentage"] < 5:
            insight += "highly stable."

        elif summary["anomaly_percentage"] < 15:
            insight += "moderately stable."

        else:
            insight += "highly anomalous."

        content.append( Paragraph( "<b>Insights</b>", styles["Heading2"], ) )

        content.append(Spacer(1, 8))

        content.append( Paragraph( insight, styles["Normal"], ) )

        content.append(Spacer(1, 20))

        chart_path = ChartService.generate_summary_chart(
            summary["normal"],
            summary["anomalies"],
        )

        content.append( Paragraph( "<b>Detection Visualization</b>", styles["Heading2"], ) )

        content.append(Spacer(1, 5))

        content.append( Image( chart_path, width=400, height=250, ) )

        content.append(Spacer(1, 10))

        pca_chart_path = ChartService.generate_pca_pdf_chart(df)

        content.append( Image( pca_chart_path, width=400, height=300, ) )

        content.append(Spacer(1, 10))

        histogram_chart = ChartService.generate_histogram_chart(df)

        content.append( Image( histogram_chart, width=400, height=300, ) )

        content.append(Spacer(1, 10))

        content.append( Paragraph( "Generated by Smart Anomaly Detection Platform", styles["Italic"], ) )

        doc.build(content)

        return response