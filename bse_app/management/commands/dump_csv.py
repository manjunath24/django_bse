from django.core.management.base import BaseCommand
import time
from django.db import IntegrityError
import csv

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from bse_app.models import Company, CompanyDetail, FileStatus




def parse_csv_file(file_path):
    file_name = file_path.split('/')[-1]
    date = file_path.split('/')[-1][2:8]
    data_reader = csv.reader(open(file_path), delimiter=',', quotechar='"')

    if FileStatus.objects.filter(file_name=file_name, is_parsed=True).exists():
        print 'File already parsed'
        return False

    for row in data_reader:
        if row[0] != 'SC_CODE':
            print 'Creating SC_CODE', row[0]
            company, created = Company.objects.get_or_create(
                sc_code=row[0], companyname=row[1])
            company_detail = CompanyDetail.objects.create(
                company=company,
                opening=row[4],
                high=row[5],
                low=row[6],
                closing=row[7],
                date=date)
    FileStatus.objects.create(file_name=file_name, is_parsed=True)
    print 'Done ....'


class Command(BaseCommand, LoggingEventHandler):

    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)
        if not event.is_directory:
            parse_csv_file(event.src_path)

    def watch_dog(self, dir_path=None):
        observer = Observer()
        observer.event_queue.maxsize = 2000
        observer.schedule(self, dir_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def handle(self, *dir_name, **options):
        self.watch_dog(dir_name[0])
