from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from classification.services.pdf_service import PDFService


@login_required
def download_classification_pdf(request):

    report = request.session.get( "classification_report" )

    if not report:
        return redirect("classification_home")

    return PDFService.generate_classification_pdf(report)