# Generated by Django 5.1.5 on 2025-01-29 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0023_alter_blockexercisedata_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ['value']},
        ),
    ]
