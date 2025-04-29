from pathlib import Path
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

recipient = "manis.shr@gmail.com"
sender = settings.EMAIL_HOST_USER
image_path = 'media/upload/logo.png'
image_name = Path(image_path).name

subject = "I am sending you nice image."
text_message = f"Email with a nice embedded image {image_name}."

html_message = f"""
<!doctype html>
    <html lang=en>
        <head>
            <meta charset=utf-8>
            <title>Some title.</title>
        </head>

        <body>
            <h1>{subject}</h1>
            <p>
            Here is my nice image.<br>
            <img src='cid:{image_name}'/>
            </p>
        </body>
    </html>
"""
text_content = """Hi"""
# the function for sending an email


def SendHTMLMail(subject, context, template_name, to_mail, from_mail, image_path=None, image_name=None):
    """Html Send Through Email"""
    context = context
    subject = subject
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_mail,
        [to_mail]
    )
    email.attach_alternative(html_content, 'text/html')
    email.content_subtype = 'html'  # set the primary content to be text/html
    # it is an important part that ensures embedding of an image
    email.mixed_subtype = 'related'

    with open(image_path, mode='rb') as f:
        image = MIMEImage(f.read())
        email.attach(image)
        image.add_header('Content-ID', f"<{image_name}>")

    return email.send()


# send an test email
# send_email(subject="TEST", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient, image_path=image_path, image_name=image_name)
