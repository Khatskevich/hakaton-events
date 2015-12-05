from django.contrib.contenttypes import forms
from django.forms import ModelForm
from event.models import Event

__author__ = 'lesaha'

class NewEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ( 'pk',)

