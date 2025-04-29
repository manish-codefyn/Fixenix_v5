from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
from django.conf import settings
import os
import re
import time
import qrcode
import requests 
import tempfile




def download_temp_image(image_url):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        for chunk in response.iter_content(1024):
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name
    return None



def qr_generate(data, size=2, version=2, border=0):
    """
    Generate a QR code and save it as a temporary file.
    Returns the absolute path of the saved QR code image.
    """
    qr = qrcode.QRCode(version=version, box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    img.save(temp_file.name)
    return temp_file.name

def fetch_resources(uri, rel):
    """
    Fetch resources for xhtml2pdf.
    Supports both local and remote media files.
    """
    if uri.startswith(settings.MEDIA_URL):  # Local media
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
        return path
    elif uri.startswith("http"):  # Remote media (e.g., Cloudinary)
        response = requests.get(uri, stream=True)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in response.iter_content(1024):
                temp_file.write(chunk)
            temp_file.close()
            return temp_file.name
    return None
# def fetch_resources(uri, rel):
#        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
#        return path

def render_to_pdf(template_src, context_dict={}, pdf_name=""):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    pdf_status = pisa.CreatePDF(html.encode("ISO-8859-1"), dest=response, link_callback=fetch_resources)

    if pdf_status.err:
        return HttpResponse("Some errors were encountered <pre>" + html + "</pre>")

    return response
# def render_to_pdf(template_src, context_dict={}, pdf_name = {}):
   
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
#     pdf_status = pisa.CreatePDF(html.encode("ISO-8859-1"), dest=response,link_callback=fetch_resources )

#     if pdf_status.err:
#         return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')

#     return response

   


    