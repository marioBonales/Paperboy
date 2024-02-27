from dotenv import dotenv_values
from imapclient import IMAPClient
import os
import email
import quopri
import pandoc
from pandoc.types import Pandoc, Meta
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import date

config = dotenv_values(".env")

FILENAME = f"Paperboy For {date.today()}.epub"

def getConfig(configName):
    return str(config[configName])


def getDocumentFromMessagePart(part):
    html = part.get_payload()
    html = quopri.decodestring(str(html))
    return pandoc.read(html, format="html")


def appendToDoc(doc, finalDoc):
    finalDoc[1] = finalDoc[1] + doc[1]
    finalDoc[0] = doc[0]
    return finalDoc


def sendEmailToKindle(filename):
    msg = MIMEMultipart()
    msg['From'] = "Paperboy <" + getConfig("EMAIL") + ">"
    msg['To'] = getConfig("KINDLE_EMAIL")
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Your paper for " + formatdate()

    msg.attach(MIMEText("Document attached"))

    with open(filename, 'rb') as file:
        basename = os.path.basename(FILENAME)
        part = MIMEApplication(file.read(), Name=basename)
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename
    msg.attach(part)

    smtp_ssl_host = getConfig("SMTP_SERVER")
    smtp_ssl_port = 465
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(getConfig("EMAIL"), getConfig("PASSWORD"))

    server.send_message(msg)
    server.quit()


# context manager ensures the session is cleaned up
with IMAPClient(host=getConfig("IMAP_SERVER")) as client:
    client.login(getConfig("EMAIL"), getConfig('PASSWORD'))
    client.select_folder(config['EMAIL_FOLDER'])

    # search criteria are passed in a straightforward way
    # (nesting is supported)
    messages = client.search("UNSEEN")

    # fetch selectors are passed as a simple list of strings.
    response = client.fetch(messages, ['BODY', 'RFC822'])

    # `response` is keyed by message id and contains parsed,
    # converted response items.
    finalDoc = Pandoc(Meta({}), [])
    for message_id, data in response.items():
        body = data[b'RFC822']
        message = email.message_from_bytes(body)
        html = ""
        for part in message.walk():
            if part.get_content_type() != "text/html":
                continue
            doc = getDocumentFromMessagePart(part)
            appendToDoc(doc, finalDoc)
            break

    pandoc.write(finalDoc, FILENAME, format="epub")
    sendEmailToKindle(FILENAME)

