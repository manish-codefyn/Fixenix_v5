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


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


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


def SendMailInHtml(subject, context, template_name, to_mail, from_mail):
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


def QrGenerate(data, size, version, border):
    qr = qrcode.QRCode(
        version=version,  # QR code version a.k.a size, None == automatic
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # lots of error correction
        box_size=size,  # size of each 'pixel' of the QR code
        border=border,  # minimum size according to spec
    )
    qr.add_data(data)
    img = qr.make_image()
    img_name = "qr" + str(time.time()) + ".png"
    img.save(settings.MEDIA_ROOT + "/QR/" + img_name)

    return img_name
