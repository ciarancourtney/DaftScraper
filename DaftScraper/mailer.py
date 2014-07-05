__author__ = 'danmalone'

import smtplib

import secrets


def sendemail(item):
    fromaddr = 'aruthar72@gmail.com'
    toaddrs = 'daft@vadimck.com'
    if isDublinApartment(item):
        msg = createMessage(item)

        # Credentials (if needed)
        username = secrets.user
        password = secrets.passW

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()


def isDublinApartment(item):
    if 'Monthly' in item['collection']:
        if 'Dublin' in item['county']:
            if item['rent'] < 2200 and '3' in item['summary']:
                return True
    return False


def createMessage(item):
    message = 'New Property:' + item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], \
              item['link'], item['photo'], item['street'], item['rent'], item['summary']
    return message