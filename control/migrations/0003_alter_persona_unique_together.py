# Generated by Django 4.2.3 on 2023-07-12 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_persona_voto'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='persona',
            unique_together={('dni', 'apellido', 'nombre', 'num_orden')},
        ),
    ]
