from django.contrib import admin

from .models import Company, CompanyDetail

class CompanyDetailAdmin(admin.StackedInline):
    model = CompanyDetail


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyDetailAdmin]
    list_display = ('companyname', 'sc_code',)
    list_filter = ['companyname']
    search_fields = ['companyname', 'sc_code']


admin.site.register(Company, CompanyAdmin)
