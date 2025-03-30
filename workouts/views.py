from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import NotFound, PermissionDenied
from datetime import date

from .serializers import ExerciseSerializer, WorkoutSerializer, BlockSerializer, BlockExerciseSerializer, BlockExerciseDataSerializer, ActivitySerializer
from .models import Exercise, Workout, Activity

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
    
    def delete(self, request, exercise_id=None): 
        try:
            target_exercise = Exercise.objects.get(id=exercise_id)

            if target_exercise.user != request.user and not request.user.is_staff:
                raise PermissionDenied({"detail": "You do not have permission to delete this exercise."})
                
            block_exercises = target_exercise.block_exercises.all()
            for block_exercise in block_exercises:
                block = block_exercise.block

                # Deletes workout and associated blocks
                block.workout.delete()

            # Deletes exercise and associated block_exercises
            target_exercise.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Exercise.DoesNotExist:
            raise NotFound({"detail": "Exercise not found."})
    
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
                "workout": workout_serializer.instance.id,
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
                    "block": block_serializer.instance.id,
                    "exercise": exercise["exercise"],
                    "position": i
                }
                
                block_exercise_serializer = BlockExerciseSerializer(data=block_exercise)

                if block_exercise_serializer.is_valid():
                    block_exercise_serializer.save()
                else:
                    return Response(block_exercise_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                for field in exercise["fields"]:
                    new_entry = {
                        "block_exercise": block_exercise_serializer.instance.id,
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
                serializer = WorkoutSerializer(workout)

                workout_response = serializer.data
                workout_response["blocks"] = [{
                        "exercises": [{
                            "exercise": block_exercise.exercise.id,
                            "fields": block_exercise.data.values_list("field", flat=True),
                            "data": {field: block_exercise.data.get(field=field).value for field in block_exercise.data.values_list("field", flat=True)}
                        } for block_exercise in block.exercises.order_by("position")]
                    } for block in blocks]
               
                return Response(workout_response, status=status.HTTP_200_OK)
            
            except Workout.DoesNotExist:
                return Response({"details": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        
        workouts = request.user.workouts
        serializer = WorkoutSerializer(workouts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, workout_id=None):
        try:
            target_workout = Workout.objects.get(id=workout_id)
        except Workout.DoesNotExist:
            raise NotFound({"detail": "Workout not found."})
        
        if target_workout.user != request.user and not request.user.is_staff:
            raise PermissionDenied({"detail": "You do not have permission to delete this workout."})
    
        target_workout.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, workout_id=None):
        try:
            workout = Workout.objects.get(pk=workout_id)
        except Workout.DoesNotExist:
            raise NotFound({"detail": "Workout not found."})
        
        new_workout = request.data
        new_workout["user"] = request.user.id
        new_workout["created_at"] = workout.created_at

        workout_serializer = WorkoutSerializer(workout, data=new_workout)

        if workout_serializer.is_valid():
            workout_serializer.save()
        else:
            return Response(workout_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        workout.blocks.all().delete()

        for i, block in enumerate(new_workout["blocks"]):
            new_block = {
                "workout": workout.id,
                "position": i
            }
          
            block_serializer = BlockSerializer(data=new_block)

            if block_serializer.is_valid():
                block_serializer.save()
            else:
                return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            for i, exercise in enumerate(block["exercises"]):
                block_exercise = {
                    "block": block_serializer.instance.id,
                    "exercise": exercise["exercise"],
                    "position": i
                }
                
                block_exercise_serializer = BlockExerciseSerializer(data=block_exercise)

                if block_exercise_serializer.is_valid():
                    block_exercise_serializer.save()
                else:
                    return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                for field in exercise["fields"]:
                    entry = {
                        "block_exercise": block_exercise_serializer.instance.id,
                        "field": field,
                        "value": exercise["data"][field]
                    }
                 
                    block_exercise_data_serializer = BlockExerciseDataSerializer(data=entry)

                    if block_exercise_data_serializer.is_valid():
                        block_exercise_data_serializer.save()
                    else:
                        return Response(block_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(workout_serializer.data, status=status.HTTP_202_ACCEPTED)
    

class ActivityView(APIView):
    def post(self, request):
        activity_entry = request.data
        activity_entry["user"] = request.user.id

        serializer = ActivitySerializer(data=activity_entry)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, activity_id=None):
        data_update = request.data
      
        try:
            target_instance = Activity.objects.get(pk=activity_id)
        except Activity.DoesNotExist:
            raise NotFound({"detail": "Activity entry not found."})

        serializer = ActivitySerializer(target_instance, data=data_update, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, activity_id=None):
        try:
            target = Activity.objects.get(pk=activity_id)
        except Activity.DoesNotExist:
            raise NotFound({"detail": "Activity entry not found."})
        
        if target.user != request.user and not request.user.is_staff:
            raise PermissionDenied({"detail": "You do not have permission to delete this entry."})
    
        target.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        # types: "all" (default) | "recent" | "period" 
        query_type = request.query_params.get('type', 'all')
  
        activities = request.user.fitness_activity.order_by("-date_scheduled")
        
        if query_type == 'recent':
            today = date.today()
            # activities = activities[:3]
            activities = activities.filter(date_scheduled__lte=today)[:3]
            
        elif query_type == 'period':
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)
            
            if start_date:
                activities = activities.filter(date_scheduled__gte=start_date)
            if end_date:
                activities = activities.filter(date_scheduled__lte=end_date)
        
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)