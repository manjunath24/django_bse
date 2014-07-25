from django.conf.urls import patterns, include, url


urlpatterns = patterns('bse_app',
    url(
        r'(?P<companycode>.*)/(?P<day>\d{2})(?P<month>\d{2})(?P<year>\d{2})/$',
         'views.get_data', name='get_data'),
)