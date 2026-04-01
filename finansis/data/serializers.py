from rest_framework import serializers
from .models import Share

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share

        fields = ['id', 'filename', 'ticker', 'date',
                  'open', 'high', 'low', 'close', 'vol']
