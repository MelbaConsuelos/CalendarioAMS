from __future__ import unicode_literals
 
from django.contrib import admin
from django.db import models
from events.models import Event 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'notes']

