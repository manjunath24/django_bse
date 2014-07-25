from django.core.management.base import BaseCommand
from django.db import IntegrityError
import csv

from bse_app.models import Company, CompanyDetail


class Command(BaseCommand):

    def handle(self, *file_name, **options):
        date = file_name[0].split('/')[9][2:8]
        data_reader = csv.reader(open(file_name[0]), delimiter=',', quotechar='"')
        print 'Reading Objects ....'
        for row in data_reader:
            if row[0] != 'SC_CODE':
                print 'Creating SC_CODE', row[0]
                company, created = Company.objects.get_or_create(
                    sc_code=row[0], companyname=row[1])
                try:
                    company_detail = CompanyDetail.objects.create(
                        company=company,
                        opening=row[4],
                        high=row[5],
                        low=row[6],
                        closing=row[7],
                        date=date)
                except IntegrityError:
                    print 'Record already exist'
        print 'Done ....'
