from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Exercise, Workout, Block, BlockExercise, BlockExerciseData, Activity

class ExerciseSerializer(ModelSerializer):
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = '__all__'

    def get_is_editable(self, obj):
        return obj.user is not None
    
class WorkoutSerializer(ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

class BlockSerializer(ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

class BlockExerciseSerializer(ModelSerializer):
    class Meta:
        model = BlockExercise
        fields = '__all__'

class BlockExerciseDataSerializer(ModelSerializer):
    class Meta:
        model = BlockExerciseData
        fields = '__all__'

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
   
    def validate(self, data):
        if 'user' in data:
            raise ValidationError({"user": "You cannot modify the user field."})
        return data