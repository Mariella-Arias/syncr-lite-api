# Generated by Django 5.1.5 on 2025-01-28 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0020_blockexercise_blockexercisedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockexercise',
            name='block',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='workouts.block'),
            preserve_default=False,
        ),
    ]
