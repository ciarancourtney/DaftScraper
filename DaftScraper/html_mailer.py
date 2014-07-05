__author__ = 'danmalone'
import smtplib
import secrets

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address

def sendemail():
    # msg = createMessage(item)
    me = 'aruthar72@gmail.com'
    you = 'danmalone123@gmail.com'
    username = secrets.user
    password = secrets.passW

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP()
    s.connect()
    # s = smtplib.SMTP('localhost')

    # s.login(username,password)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())

    s.quit()

def createMessage(item):
    message = 'New Property:' + item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], \
              item['link'], item['photo'], item['street'], item['rent'], item['summary']
    return message

def main():
    sendemail()

if __name__ == "__main__":
    main()

