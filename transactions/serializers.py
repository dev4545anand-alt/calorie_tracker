from rest_framework import serializers
from transactions.models import Calorie




class CalorieSerializer(serializers.ModelSerializer):

    class Meta:

        model = Calorie

        fields = "__all__"

        read_only_fields = ["id","owner","created_at"]