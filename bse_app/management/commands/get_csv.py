from django.core.management.base import BaseCommand
import urllib
import os
import zipfile
from datetime import datetime
import shutil


def get_date():
    day = datetime.now().day
    month = datetime.now().month
    if month < 10:
        month = '0%s' % month
    year = datetime.now().strftime('%y')
    return '%s%s%s' % (day, month, year)


class Command(BaseCommand):

    def handle(self, **options):
        date = get_date()
        pull_from = "http://www.bseindia.com/download/BhavCopy/Equity/EQ%s_CSV.ZIP" % (date)
        push_to = "downloads/EQ%s.zip" % (date)
        url_obj = urllib.URLopener()
        try:
            url_obj.retrieve(pull_from, push_to)
        except IOError:
            print 'File not found on %s' % date
        else:
            zf = zipfile.ZipFile(push_to, 'r')
            zf.extractall('downloads/')
            shutil.move('downloads/EQ%s.CSV' % (date), 'bse_app/management/commands/csvs/')
