from rest_framework import serializers

from .models import Client, Distribution, Messages


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"

