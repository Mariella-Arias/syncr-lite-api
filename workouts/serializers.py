from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Exercises, Workouts

class ExercisesSerializer(ModelSerializer):
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = Exercises
        fields = '__all__'

    def get_is_editable(self, obj):
        return obj.user is not None
    
class WorkoutsSerializer(ModelSerializer):
    class Meta:
        model = Workouts
        fields = '__all__'