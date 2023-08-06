from typing import List
# from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# import aiosmtplib


def send_message(msg_text: str,
                 sender: str,
                 password: str,
                 recipients: List[str],
                 port: int = 587,
                 hostname: str = 'smtp.yandex.ru',
                 subject: str = 'Accommodation'):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_text))

    mailserver = smtplib.SMTP(hostname, port)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(user=sender, password=password)
    mailserver.sendmail(sender, recipients, msg.as_string())
    mailserver.quit()

# async def send_message(msg_text: str,
#                        sender: str,
#                        password: str,
#                        recipients: List[str],
#                        port: int = 587,
#                        hostname: str = 'smtp.yandex.ru',
#                        use_tls: bool = False,
#                        subject: str = 'Accommodation'):
#     message = EmailMessage()
#     message['From'] = sender
#     message['To'] = ', '.join(recipients)
#     message['Subject'] = subject
#     message.set_content(msg_text)
#
#     await aiosmtplib.send(message,
#                           sender=sender,
#                           hostname=hostname, port=port, use_tls=use_tls,
#                           recipients=recipients, password=password)
# #
# #
# from typing import List, Tuple
# import logging
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# logger = logging.getLogger(__name__)
#
#
# def send_notification(message: str, msg_to: List[str], from_email: str, auth: Tuple[str, str]):
#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['To'] = ', '.join(msg_to)
#     msg['Subject'] = 'Accommodation offer'
#     msg.attach(MIMEText(message))
#
#     mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
#
#     try:
#         mailserver.ehlo()
#         mailserver.starttls()
#         mailserver.ehlo()
#         mailserver.login(*auth)
#         mailserver.sendmail(from_email, msg_to, msg.as_string())
#         mailserver.quit()
#     except Exception as err:
#         logger.exception(err)
#         raise Exception(err)
