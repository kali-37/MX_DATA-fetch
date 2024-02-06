from django.contrib import admin

# Register your models here.
from .models import UnverifiedData, Domain, MXRecordAll, MailServerHistorical,MailServercurrent,MXRecordcurrent,Country,State


admin.site.register(UnverifiedData)

admin.site.register(Domain)
admin.site.register(MXRecordcurrent)
admin.site.register(MailServercurrent)

admin.site.register(MXRecordAll)
admin.site.register(MailServerHistorical)
admin.site.register(Country)
admin.site.register(State)
