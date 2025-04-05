import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import Config

from utils.exceptions.exception import ErrorSendingEmail


class MailingService:
    def __init__(self):
        self.sender = Config.HOST_MAIL
        self.password = Config.HOST_PASSWORD
        self.host = Config.HOST_SERVER
        self.port = Config.HOST_PORT
        self.message = MIMEMultipart("alternative")

    async def send(self, body, email, subject):
        self.message["From"] = self.sender
        self.message["To"] = email
        self.message["Subject"] = subject

        to_send = MIMEText(body, "html")
        self.message.attach(to_send)
        text = self.message.as_string()
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self.host, self.port, context=context)
        server.login(self.sender, self.password)
        try:
            error_controller = server.sendmail(self.sender, email, text)
            if len(error_controller) != 0:
                raise ErrorSendingEmail(f"Error sending mail to {email}")
        except Exception:
            raise ErrorSendingEmail(f"Error sending mail to {email}")
        finally:
            server.quit()
