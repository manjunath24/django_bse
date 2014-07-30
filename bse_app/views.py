from django.shortcuts import render, HttpResponse
from django.http import Http404
import json

from .models import Company, CompanyDetail

from graphos.sources.model import ModelDataSource
from graphos.renderers import gchart


def get_data(request, companycode=None, day=None, month=None, year=None):
    try:
        company = Company.objects.get(sc_code=companycode)
    except Company.DoesNotExist:
        raise Http404
    else:
        date = '%s%s%s' % (day, month, year)
        company_details = list(
            company.companydetail_set.filter(date=date).values(
                'opening', 'closing', 'company__companyname',))
        data = json.dumps(company_details, indent=2)
    return HttpResponse(data, content_type='application/json')


def get_graph(request,
              companycode=None,
              day_one=None,
              month_one=None,
              year_one=None,
              day_two=None,
              month_two=None,
              year_two=None):
    try:
        company = Company.objects.get(sc_code=companycode)
    except Company.DoesNotExist:
        raise Http404
    else:
        date_one = '%s%s%s' % (day_one, month_one, year_one)
        date_two = '%s%s%s' % (day_two, month_two, year_two)
        company_details = company.companydetail_set.filter(date__range=[day_one, date_two])
        data_source = ModelDataSource(company_details,
                                      fields=['opening', 'closing'])
        options = {"title": "BSE Sensex"}
        chart = gchart.LineChart(data_source, options=options)
        return render(request, 'chart.html', {'chart': chart})
