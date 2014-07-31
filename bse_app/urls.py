from django.conf.urls import patterns, include, url


urlpatterns = patterns('bse_app',
    url(r'(?P<companycode>.*)/(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{2})/$',
         'views.get_data', name='get_data'),
    # url(r'(?P<companycode>.*)/(?P<day_one>\d{2})(?P<month_one>\d{2})(?P<year_one>\d{2})/(?P<day_two>\d{2})(?P<month_two>\d{2})(?P<year_two>\d{2})/graph/$',
    #      'views.get_graph', name='get_graph'),
    url(r'marketwatch/$', 'views.market_watch', name='marketwatch'),
    url(r'marketwatch/(?P<top_trades>[\w-]+)/$', 'views.market_watch', name='marketwatch_toptrades'),
    url(r'graph/$', 'views.graph', name='graph'),
    )