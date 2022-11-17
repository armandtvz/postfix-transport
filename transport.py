import sys
import email
import base64
from datetime import datetime, timedelta, timezone, tzinfo
from email.policy import default
from email.parser import FeedParser
from email import utils




def bytes_to_b64(value):
    """
    Converts byte data to it's base64 representation.
    """
    if not value:
        return ''
    encoded = base64.b64encode(value).decode('utf-8')
    return encoded




def main(email_input=None):
    msg = None
    if not email_input:
        email_input = sys.stdin.readlines()
        email_input_plain = ''.join(email_input)

    parser = FeedParser(policy=default)
    for line in email_input:
        parser.feed(line)
    msg = parser.close()

    body = msg.get_body(preferencelist=['plain', 'html'])
    decoded_body = body.get_payload(decode=True)
    body = decoded_body.decode()

    attachments = []
    attachment_content_types = [
        'image/jpeg',
        'image/png',
        'application/octet-stream',
    ]
    for part in msg.iter_attachments():
        content_type = part.get_content_type()
        if content_type in attachment_content_types:
            filename = part.get_filename()
            img_bytes = part.get_payload(decode=True)
            b64_image = bytes_to_b64(img_bytes)
            attachments.append(b64_image)
    print(len(attachments), 'attachments found')




if __name__ == '__main__':
    with open('test_email.eml') as f:
        email_input = f.read()
    main(email_input)
