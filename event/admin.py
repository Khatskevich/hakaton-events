from django.contrib import admin

# Register your models here.
from event.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lng', 'time',)
    # list_filter = ( 'type_of_user', 'status_of_registration')
    # search_fields = ['phone','first_name', 'last_name', 'email' ]


admin.site.register(Event, EventAdmin)
