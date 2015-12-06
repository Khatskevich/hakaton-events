import datetime
from haystack import indexes
from event.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    description = indexes.CharField()
    title = indexes.CharField(model_attr='title')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())