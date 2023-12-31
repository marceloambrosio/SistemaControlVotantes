# Generated by Django 4.2.3 on 2023-09-12 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_remove_tipoeleccion_cargo_cargo_orden_cargo'),
        ('computo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='partido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='computo.partido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidatoeleccion',
            name='candidato',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='computo.candidato'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidatoeleccion',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='control.cargo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidatoeleccion',
            name='eleccion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='control.eleccion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='computo',
            name='eleccion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='control.eleccion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallecomputo',
            name='mesa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='control.mesa'),
            preserve_default=False,
        ),
    ]
