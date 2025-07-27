
from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    recipient = filters.NumberFilter(field_name="recipient__id")
    sender_id = filters.NumberFilter(field_name="sender__id")
    sender_username = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['recipient', 'sender_id', 'sender_username', 'start_date', 'end_date']
