from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
