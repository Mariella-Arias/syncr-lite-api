# Generated by Django 5.1.5 on 2025-01-27 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0019_rename_blocks_block'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='BlockExerciseData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=20)),
                ('value', models.IntegerField()),
                ('block_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='workouts.blockexercise')),
            ],
        ),
    ]
