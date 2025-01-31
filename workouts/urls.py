from django.urls import path

from . import views

urlpatterns = [
    path('activity/<int:activity_id>/', views.ActivityView.as_view(), name='fitness-activity-entry'),
    path('activity/', views.ActivityView.as_view(), name='fitness-activity'),
    path('exercises/<int:exercise_id>/', views.ExercisesList.as_view(), name='delete-exercise'),
    path('exercises/', views.ExercisesList.as_view(), name='exercises-list'),
    path('<int:workout_id>/', views.WorkoutsList.as_view(), name='workout-detail'),
    path('', views.WorkoutsList.as_view(), name='workouts-list')
]
