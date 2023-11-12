from rest_framework import serializers

from reservations.models import ActivitySubscription


class CreateReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ActivitySubscription
        fields = ['user', 'type', 'hour', 'weekday']
