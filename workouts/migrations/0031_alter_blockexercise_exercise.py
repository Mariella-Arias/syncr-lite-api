# Generated by Django 5.1.5 on 2025-02-03 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0030_alter_activity_workout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockexercise',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='block_exercises', to='workouts.exercise'),
        ),
    ]
