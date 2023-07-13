# Generated by Django 4.2.3 on 2023-07-13 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='circuito',
            name='id',
        ),
        migrations.RemoveField(
            model_name='seccion',
            name='id',
        ),
        migrations.AlterField(
            model_name='circuito',
            name='num_circuito',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='seccion',
            name='num_seccion',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
