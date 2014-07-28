from django.contrib import admin

from .models import Company, CompanyDetail, FileStatus

class CompanyDetailAdmin(admin.StackedInline):
    model = CompanyDetail


class CompanyAdmin(admin.ModelAdmin):
    inlines = [CompanyDetailAdmin]
    list_display = ('companyname', 'sc_code',)
    list_filter = ['companyname']
    search_fields = ['companyname', 'sc_code']


class FileStatusAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'is_parsed')


admin.site.register(Company, CompanyAdmin)
admin.site.register(FileStatus, FileStatusAdmin)
