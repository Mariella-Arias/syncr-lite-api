from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q

from .serializers import ExerciseSerializer, WorkoutSerializer, BlockSerializer, BlockExerciseSerializer, BlockExerciseDataSerializer
from .models import Exercise, Workout

User = get_user_model()

class ExercisesList(APIView):
    def post(self, request):
        new_exercise = request.data
        serializer = ExerciseSerializer(data=new_exercise)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        exercises = Exercise.objects.filter(Q(user=request.user) | Q(user__isnull=True))
        serializer = ExerciseSerializer(exercises, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WorkoutsList(APIView):
    def post(self, request):
        new_workout = request.data
        new_workout["user"] = request.user.id

        workout_serializer = WorkoutSerializer(data=new_workout)

        # Create workout
        if workout_serializer.is_valid():
            workout_serializer.save()
        else:
            return Response(workout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create blocks
        for i, block in enumerate(new_workout["blocks"]):
            new_block = {
                "workout": workout_serializer.data["id"],
                "position": i
            }

            block_serializer = BlockSerializer(data=new_block)

            if block_serializer.is_valid():
                block_serializer.save()
            else:
                return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Create block exercises
            for i, exercise in enumerate(block["exercises"]):
                block_exercise = {
                    "block": block_serializer.data["id"],
                    "exercise": exercise["exercise"],
                    "position": i
                }
                
                block_exercise_serializer = BlockExerciseSerializer(data=block_exercise)

                if block_exercise_serializer.is_valid():
                    block_exercise_serializer.save()
                else:
                    return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                for field in exercise["fields"]:
                    new_entry = {
                        "block_exercise": block_exercise_serializer.data["id"],
                        "field": field,
                        "value": exercise["data"][field]
                    }
                 
                    block_exercise_data_serializer = BlockExerciseDataSerializer(data=new_entry)

                    if block_exercise_data_serializer.is_valid():
                        block_exercise_data_serializer.save()
                    else:
                        return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(workout_serializer.data, status=status.HTTP_201_CREATED)
   
    def get(self, request, workout_id=None):
        if workout_id:
            try:
                workout = Workout.objects.get(id=workout_id)
                blocks = workout.blocks.order_by("position")

                result = {
                    "id" : workout_id,
                    "name": workout.name,
                    "blocks": [{
                        "exercises": [{
                            "exercise": block_exercise.exercise.id,
                            "fields": block_exercise.data.values_list("field", flat=True),
                            "data": {field: block_exercise.data.get(field=field).value for field in block_exercise.data.values_list("field", flat=True)}
                        } for block_exercise in block.exercises.order_by("position")]
                    } for block in blocks]
                }

                serializer = WorkoutSerializer(workout)

                return Response(result, status=status.HTTP_200_OK)
            except Workout.DoesNotExist:
                return Response({"details": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        
        workouts = request.user.workouts
        serializer = WorkoutSerializer(workouts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
