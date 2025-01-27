from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class Exercises(models.Model):
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