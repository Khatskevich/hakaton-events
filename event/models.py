from django.db import models


class Event(models.Model):

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    SITE_CHOICES = (
        ('VK', 'vk.com'),
        ('FB', 'facebook.com'),
    )

    def get_external_url(self):
        site_url = [s[1] for s in self.SITE_CHOICES if s[0] == self.site][0]
        if self.site == 'VK':
            return '/'.join(['https:/', site_url, "club%s" % self.ext_id])
        elif self.site == 'FB':
            return '/'.join(['https:/', site_url, "events", self.ext_id])

    lat = models.FloatField(help_text="Latitude of the center")
    lng = models.FloatField(help_text="Longitude of the center")
    start_date = models.DateTimeField(help_text="Start date of the event")
    end_date = models.DateTimeField(help_text="Start date of the event", blank=True)
    photo = models.CharField(max_length=255, help_text="Preview", default="")
    ext_id = models.CharField(max_length=255,
                              help_text="ID from FB or VK",
                              unique=True)
    site = models.CharField(max_length=2, choices=SITE_CHOICES)
    title = models.CharField(max_length=255, help_text="Title of the event")
    description = models.TextField(help_text="Event description text", blank=True)
    member_count = models.IntegerField(help_text="Number of event members")
    category = models.CharField(max_length=255, help_text="The category of the event")
