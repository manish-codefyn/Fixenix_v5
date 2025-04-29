from django.conf import settings

# Path
from pathlib import Path
from email.mime.image import MIMEImage

# mail
from django.core.mail import EmailMultiAlternatives

# template rendering
from django.template import loader
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# QR CODE
import io
import qrcode
import time
import datetime
# PDF
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

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


def ShowPDF(template_src, context_dict={}, pdf_name={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    pdf_status = pisa.CreatePDF(
        html.encode("ISO-8859-1"), dest=response, link_callback=fetch_resources
    )

    if pdf_status.err:
        return HttpResponse("Some errors were encountered <pre>" + html + "</pre>")

    return response


def RenderToPDF(template_src, context_dict={}, pdf_name={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    with open(pdf_name, "wb+") as output:
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), output, link_callback=fetch_resources
        )
    return output.name


def SendMailWithImg(subject, context, template_name, to_mail, from_mail, images=()):
    """Html Send Through Email"""
    context = context
    subject = subject
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_mail, [to_mail])
    email.attach_alternative(html_content, "text/html")
    email.content_subtype = "html"  # set the primary content to be text/html
    email.mixed_subtype = (
        "related"  # it is an important part that ensures embedding of an image
    )

    with open(image_path, mode="rb") as f:
        image = MIMEImage(f.read())
        email.attach(image)
        image.add_header("Content-ID", f"<{image_name}>")

    return email.send(fail_silently=False)


def send_html_mail(subject, context, template_name, to_mail, from_mail):
    """Html Send Through Email"""
    context = context
    subject = subject
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, text_content, from_mail, [to_mail])
    email.attach_alternative(html_content, "text/html")
    return email.send(fail_silently=False)


def SendPDFInMail(subject, template_name, content, from_mail, to_mail, pdf_file):
    # """Html Send Through Email"""
    # send_mail = EmailMessage(
    # subject, 'context',
    # from_mail ,
    # [to_mail]
    # )
    # send_mail.attach_file(str(pdf_file))
    # return send_mail.send()

    """Html,PDF Send Through Email"""
    context = content
    subject = subject
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_mail, [to_mail])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(pdf_file)
    return msg.send()

