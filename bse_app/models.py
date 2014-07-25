from django.db import models


class Company(models.Model):
    sc_code = models.IntegerField()
    companyname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.companyname



class CompanyDetail(models.Model):
    company = models.ForeignKey(Company)
    opening = models.CharField(max_length=750)
    high = models.CharField(max_length=750)
    low = models.CharField(max_length=750)
    closing = models.CharField(max_length=750)
    date = models.CharField(max_length=750)

    class Meta:
        unique_together = ('company', 'date')

    def __unicode__(self):
        return self.date

