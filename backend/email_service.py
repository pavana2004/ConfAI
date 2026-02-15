# # GMAIL_USER = "pav.howdy@gmail.com"
# # GMAIL_APP_PASSWORD = "anll lvti gxfb bopv"



# import smtplib
# from email.message import EmailMessage

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587




# def send_email(to_emails: list[str], subject: str, body: str):
#     msg = EmailMessage()
#     msg["From"] = GMAIL_USER
#     msg["To"] = ", ".join(to_emails)
#     msg["Subject"] = subject
#     msg.set_content(body)

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.send_message(msg)



# import smtplib
# from email.message import EmailMessage

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# GMAIL_USER = "rajitkumaran27@gmail.com"
# GMAIL_APP_PASSWORD = "buaj yfkv eran izje"


# from email.message import EmailMessage
# import smtplib

# def send_email(to_emails, subject, body, ics_content=None):
#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = GMAIL_USER
#     msg["To"] = ", ".join(to_emails)
#     msg.set_content(body)

#     if ics_content:
#         msg.add_attachment(
#             ics_content,
#             subtype="calendar",
#             maintype="text",
#             filename="meeting.ics"
#         )

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         smtp.send_message(msg)

from email.message import EmailMessage
import smtplib
GMAIL_USER = "pav.howdy@gmail.com"
GMAIL_APP_PASSWORD = "anll lvti gxfb bopv"

def send_email(
    to_emails: list[str],
    subject: str,
    body: str,
    ics_content: str | None = None
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "confai@yourdomain.com"
    msg["To"] = ", ".join(to_emails)

    msg.set_content(body)

    if ics_content:
        msg.add_attachment(
            ics_content,
            subtype="calendar",
            filename="meeting.ics"
        )

        # 🔑 THIS is where METHOD goes
        for part in msg.iter_attachments():
            part.replace_header(
                "Content-Type",
                "text/calendar; method=REQUEST; charset=UTF-8"
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
