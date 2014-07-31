from django.shortcuts import render, HttpResponse
from django.http import Http404
import json
from django.db.models import Max
from django.core.paginator import Paginator

from .models import Company, CompanyDetail
from .forms import GraphForm

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
                'opening',
                'closing',
                'company__companyname',
                'prev_close',
                'no_of_shares',
                'net_turnover',
                'date',))
        data = json.dumps(company_details, indent=2)
    return HttpResponse(data, content_type='application/json')


# def get_graph(request,
#               companycode=None,
#               day_one=None,
#               month_one=None,
#               year_one=None,
#               day_two=None,
#               month_two=None,
#               year_two=None):
#     try:
#         company = Company.objects.get(sc_code=companycode)
#     except Company.DoesNotExist:
#         raise Http404
#     else:
#         date_one = '%s%s%s' % (day_one, month_one, year_one)
#         date_two = '%s%s%s' % (day_two, month_two, year_two)
#         company_details = company.companydetail_set.filter(date__range=[day_one, date_two])
#         data_source = ModelDataSource(company_details,
#                                       fields=['opening', 'closing'])
#         options = {"title": "BSE Equity Market"}
#         chart = gchart.LineChart(data_source, options=options)
#         return render(request, 'chart.html', {'chart': chart})


def market_watch(request, top_trades=None):
    top_trade = False
    max_date = CompanyDetail.objects.all().aggregate(Max('date'))
    records = CompanyDetail.objects.filter(date=max_date['date__max']).order_by('-net_turnover')
    if top_trades:
        records = CompanyDetail.objects.filter(date=max_date['date__max']).order_by('-no_of_shares')
        top_trade = True
    paginator = Paginator(records, 25)
    page = request.GET.get('page', '1')
    records_pagination = paginator.page(page)
    return render(request, 'market.html', {'records': records_pagination, 'top_trade': top_trade})


def graph(request):
    form = GraphForm(request.GET)
    context = {'form': form}
    if form.is_valid():
        data = form.cleaned_data
        start_day = data['start_date'].day
        start_month = data['start_date'].month
        if start_month < 10:
            start_month = '0%s' % start_month
        start_year = data['start_date'].strftime('%y')

        end_day = data['end_date'].day
        end_month = data['end_date'].month
        if end_month < 10:
            end_month = '0%s' % end_month
        end_year = data['end_date'].strftime('%y')

        start_date = '%s%s%s' % (start_day, start_month, start_year)
        end_date = '%s%s%s' % (end_day, end_month, end_year)

        try:
            company = Company.objects.get(companyname=data['company_name'])
        except Company.DoesNotExist:
            raise Http404
        else:
            company_details = company.companydetail_set.filter(date__range=[start_date, end_date])
            data_source = ModelDataSource(company_details,
                                          fields=['opening', 'closing'])
            options = {"title": "BSE Equity Market"}
            chart = gchart.LineChart(data_source, options=options)
            context['chart'] = chart
    return render(request, 'graph.html', context)
