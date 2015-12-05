from django.db import models


class Event(models.Model):

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    def get_external_url(self):
        if self.site == 'vk.com':
            return '/'.join(['https:/', self.site, "club%s" % self.ext_id])
        elif self.site == 'facebook.com':
            return '/'.join(['https:/', self.site, "events", self.ext_id])

    SITE_CHOICES = (
        ('VK', 'vk.com'),
        ('FB', 'facebook.com'),
    )

    lat = models.FloatField(help_text="Latitude of the center")
    lng = models.FloatField(help_text="Longitude of the center")
    start_date = models.DateTimeField(help_text="Start date of the event")
    photo = models.CharField(max_length=255, help_text="Preview")
    ext_id = models.CharField(max_length=255,
                              help_text="ID from FB or VK",
                              unique=True)
    site = models.CharField(max_length=2, choices=SITE_CHOICES)
    title = models.CharField(max_length=255, help_text="Title of the event")
