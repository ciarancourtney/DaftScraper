__author__ = 'danmalone'

import smtplib
from DaftScraper import settings


def _isDublinApartment(item):
    if 'Monthly' in item['collection']:
        if 'Dublin' in item['county']:
            if item['rent'] < 2200 and '3' in item['summary']:
                return True
    return False


def _createMessage(item):
    message = 'New Property:' + item['area'], item['collection'], item['county'], item['id'], item['lat'], item['long'], \
              item['link'], item['photo'], item['street'], item['rent'], item['summary']
    return message


def sendemail(item):
    if _isDublinApartment(item):
        msg = _createMessage(item)

        # The actual mail send
        server = smtplib.SMTP(settings.EMAIL_CONF['smtp_server'])
        server.starttls()
        server.login(settings.EMAIL_CONF['username'], settings.EMAIL_CONF['password'])
        server.sendmail(settings.EMAIL_CONF['from'], settings.EMAIL_CONF['to'], msg)
        server.quit()
