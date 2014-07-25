from django.shortcuts import render, HttpResponse
from django.http import Http404
import json

from .models import Company, CompanyDetail


def get_data(request, companycode=None, day=None, month=None, year=None):
    try:
        company = Company.objects.get(sc_code=companycode)
    except Company.DoesNotExist:
        raise Http404
    else:
        date = '%s%s%s' % (day, month, year)
        company_details = list(
            company.companydetail_set.filter(date=date).values(
                'opening', 'closing', 'high', 'low', 'company__companyname',))
        data = json.dumps(company_details, indent=2)
    return HttpResponse(data, content_type='application/json')
