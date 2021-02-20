from rest_framework import serializers
from .models import PlayerStatistic


class PlayerStatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayerStatistic
        fields = '__all__'
