import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import io

class EmailSender():

    def __init__(self, host=None, port=None, user=None, password=None, fromaddr=None):
        self.mailhost = host
        self.mailport = port
        self.user = user
        self.password = password
        self.fromaddr = fromaddr

    def get_smtp_port(self):
        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        return port

    def get_recipients(self, toaddrs):
        recipients = ';'.join(
            [toaddrs] if not isinstance(toaddrs, list) else toaddrs
        )
        return recipients

    def create_smtp(self):
        port = self.get_smtp_port()
        return smtplib.SMTP(self.mailhost, port)

    def build_message(self, recipients, subject, message,logo):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = recipients
        msg['Subject'] = Header(subject, 'utf-8')
        msg.attach(MIMEText(message.strip(), 'html','utf-8'))

        msgImage = None
        with io.open(logo, 'rb') as fp:
            msgImage = MIMEImage(fp.read())

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<logo>')
        msg.attach(msgImage)

        return msg
    
    def setup_security(self, smtp):
        def is_tls(port):
            return '587' == port
        if is_tls(self.get_smtp_port()):
            smtp.ehlo() 
            smtp.starttls()
            smtp.ehlo()
        if self.user and self.password:
            smtp.login(self.user, self.password)

    def send(self, toaddres, subject, content,logo):
        recipients = self.get_recipients(toaddres)
        msg = self.build_message(recipients, subject, content, logo)
        smtp = self.create_smtp()
        self.setup_security(smtp)
        smtp.sendmail(self.fromaddr, recipients.split(';'), msg.as_string())
        smtp.quit()
