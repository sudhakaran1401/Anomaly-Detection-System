import os
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from anomaly.models import DetectionHistory
from anomaly.services.pdf_service import PdfService
from anomaly.services.pseudo_label_service import PseudoLabelService


@login_required
def download_csv(request):

    file_path = request.session.get("result_file")

    if not file_path or not os.path.exists(file_path):
        return HttpResponse("No data found")

    df = pd.read_csv(file_path)

    df = PseudoLabelService.generate(df)

    uploaded_filename = request.session.get(
        "uploaded_filename",
        "dataset.csv",
    )

    filename, _ = os.path.splitext(uploaded_filename)

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}_labelled.csv"'
    )

    df.to_csv(response, index=False)

    return response


@login_required
def download_pdf(request):
    return PdfService.generate_anomaly_pdf(request)


@login_required
def history(request):

    history_data = DetectionHistory.objects.order_by(
        "-created_at"
    )[:20]

    return render(
        request,
        "history.html",
        {
            "history_data": history_data,
        },
    )


@login_required
def dashboard(request):
    return render(request, "result.html")


@login_required
def clear_history(request, id=None):

    if id:
        get_object_or_404(
            DetectionHistory,
            id=id,
        ).delete()
    else:
        DetectionHistory.objects.all().delete()

    return redirect("history")