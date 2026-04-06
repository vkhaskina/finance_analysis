from rest_framework import serializers
from .models import Share

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share

        fields = ['id', 'filename', 'ticker', 'period', 'date',
                  'open', 'high', 'low', 'close', 'vol',
                  'profit_simple', 'profit_ln']
