from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
def send_email_notification(decision):

    # render the HTML content.
    if decision == 'approved':
        html_content = render_to_string(
            "emails/approved_email.html",
            context={"name": "lego"}
        )
    else:
        html_content = render_to_string(
            "emails/rejected_email.html",
            context={"name": "lego"}
        )

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        subject="Subject here",
        body=html_content,
        from_email="sales@expensely.net",
        to=["sales@expensely.net"],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.send()