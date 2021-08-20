from django.contrib import admin
from DataStorage.models import Data
# Register your models here.


class AdminData(admin.ModelAdmin):

    list_display = ['key', 'format_value', 'createtime']


admin.site.site_title = '数据存储'
admin.site.site_header = '数据存储'
admin.site.register(Data, AdminData)
