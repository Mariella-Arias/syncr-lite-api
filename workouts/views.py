from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q

from .serializers import ExercisesSerializer
from .models import Exercises

User = get_user_model()

class ExercisesList(APIView):
    def post(self, request):
        new_exercise = request.data
        serializer = ExercisesSerializer(data=new_exercise)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        exercises = Exercises.objects.filter(Q(user=request.user) | Q(user__isnull=True))
        serializer = ExercisesSerializer(exercises, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)