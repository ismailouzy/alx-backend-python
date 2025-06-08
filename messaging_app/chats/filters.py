import django_filters
from .models import Message
from django.utils import timezone
from datetime import timedelta


class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__username')
    start_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    last_24_hours = django_filters.BooleanFilter(method='filter_last_24_hours')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']

    def filter_last_24_hours(self, queryset, name, value):
        if value:
            return queryset.filter(timestamp__gte=timezone.now() - timedelta(hours=24)
        return queryset
