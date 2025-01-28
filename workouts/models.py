from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class Exercise(models.Model):
    PARAM_CHOICES = [('reps', 'Repetitions'), ('duration', 'Duration')]

    label = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    tracking_param = models.CharField(choices=PARAM_CHOICES, default="reps")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["value", "user"], condition=Q(user__isnull=False), name="unique_user_generated_exercise"),
            models.UniqueConstraint(fields=["value"], condition=Q(user__isnull=True), name="unique_default_exercise")
        ]

    def __str__(self):
        return self.value

class Workout(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="workouts")

    def __str__(self):
        return f"Template: {self.name} by {self.user}"
    
class Block(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="blocks")
    position = models.IntegerField(null=False)

    def __str__(self):
        return f"Block {self.position} in {self.workout.name}"
    
class BlockExercise(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    position = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.exercise.value} in Block {self.block.position}, position {self.position}"
    
class BlockExerciseData(models.Model):
    block_exercise = models.ForeignKey(BlockExercise, on_delete=models.CASCADE, related_name="data")
    field = models.CharField(max_length=20)
    value = models.IntegerField() # This will actually be either Integer or duration

    def __str__(self):
        return f"{self.field}: {self.value} for {self.block_exercise.exercise.value}"