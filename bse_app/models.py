from django.db import models


class Company(models.Model):
    sc_code = models.IntegerField()
    companyname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.companyname



class CompanyDetail(models.Model):
    company = models.ForeignKey(Company)
    opening = models.FloatField(max_length=100)
    high = models.CharField(max_length=100)
    low = models.CharField(max_length=100)
    closing = models.FloatField(max_length=100)
    prev_close = models.FloatField(max_length=100)
    no_trades = models.FloatField(max_length=100)
    no_of_shares = models.FloatField(max_length=100)
    net_turnover = models.FloatField(max_length=100)
    date = models.CharField(max_length=100)

    class Meta:
        unique_together = ('company', 'date')

    def __unicode__(self):
        return self.date


class FileStatus(models.Model):
    file_name = models.CharField(max_length=100)
    is_parsed = models.BooleanField()

    def __unicode__(self):
        return self.file_name

