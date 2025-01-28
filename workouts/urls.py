from django.urls import path

from . import views

urlpatterns = [
    path('exercises/', views.ExercisesList.as_view(), name='exercises-list'),
    path('', views.WorkoutsList.as_view(), name='workouts-list'),
    path('<int:workout_id>/', views.WorkoutsList.as_view(), name='workout-detail')
]
