from django.contrib import admin

# Register your models here.
from event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'lat', 'lng', 'start_date', 'site', 'ext_id',)
    list_filter = ( 'site',)
    search_fields = ['description','title' ]


admin.site.register(Event, EventAdmin)
