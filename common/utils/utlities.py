#
#
#
# def send_email(to, subject, body, attachment=None, reply_to=None):
#     import smtplib
#     import email.utils
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     # Replace sender@example.com with your "From" address.
#     # This address must be verified.
#     SENDER = config.SENDER_EMAIL
#     SENDERNAME = config.SENDER_NAME
#     REPLY_TO_ADDRESS = config.REPLY_TO_ADDRESS
#     # Replace recipient@example.com with a "To" address. If your account
#     # is still in the sandbox, this address must be verified.
#     RECIPIENT = to
#     # Replace smtp_username with your Amazon SES SMTP user name.
#     USERNAME_SMTP = config.MAIL_USERNAME
#     # Replace smtp_password with your Amazon SES SMTP password.
#     PASSWORD_SMTP = config.MAIL_PASSWORD
#     HOST = config.MAIL_SERVER
#     PORT = config.MAIL_PORT
#
#     # Create message container - the correct MIME type is multipart/alternative.
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     if attachment:
#         msg['Attachment'] = attachment
#         part = MIMEBase('application', "octet-stream")
#         part.set_payload(open("invoice.pdf", "rb").read())
#         part.add_header('Content-Disposition', 'attachment; filename="invoice.pdf"')
#         part.add_header('reply-to', 'support@duruper.com')
#         encoders.encode_base64(part)
#         msg.attach(part)
#     msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
#     msg['To'] = RECIPIENT
#     part2 = MIMEText(body, 'html')
#     if reply_to:
#         msg.add_header('reply-to', reply_to)
#     else:
#         msg.add_header('reply-to', REPLY_TO_ADDRESS)
#     msg.attach(part2)
#
#     try:
#         server = smtplib.SMTP(HOST, PORT)
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login(USERNAME_SMTP, PASSWORD_SMTP)
#         server.sendmail(SENDER, RECIPIENT, msg.as_string())
#         server.close()
#     except Exception as e:
#         print("Error: ", e)
#     else:
#         print("Email sent!")