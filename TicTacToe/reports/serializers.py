from rest_framework import serializers
from django_db_logger.models import StatusLog


class LoggerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusLog
        fields = '__all__'
