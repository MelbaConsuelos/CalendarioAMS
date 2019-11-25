from __future__ import unicode_literals
 
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from model_utils import Choices

class Room(models.Model):
    room_name = models.CharField('Room Name', max_length=100)

    def __str__(self):
        return self.room_name

class Venue(models.Model):
    venue_name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300, default='not specified')
    phone = models.CharField('Contact Phone', max_length=20, blank=True)
    web = models.URLField('Web Address', blank=True)
    room_name = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.venue_name

class Venue_Room(models.Model):
    belonging_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    belonging_room_name = models.CharField('Room Name', max_length=100)

    def __str__(self):
        return self.belonging_room_name

  

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    venue_name = models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    #manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)


     
    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.event_name))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

    def __str__(self):
         return self.event_name


