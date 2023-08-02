# Generated by Django 4.2.3 on 2023-08-02 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bocadeurna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidato',
            name='partido',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='bocadeurna.partido'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidato',
            name='apellido',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='candidato',
            name='nombre',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='titulo',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='partido',
            name='nombre',
            field=models.CharField(),
        ),
    ]
