# Generated by Django 4.2.3 on 2023-09-05 23:47

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Circuito',
            fields=[
                ('num_circuito', models.IntegerField(primary_key=True, serialize=False)),
                ('localidad', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Escuela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.circuito')),
            ],
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_mesa', models.IntegerField()),
                ('escuela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.escuela')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('num_seccion', models.IntegerField(primary_key=True, serialize=False)),
                ('departamento', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoEleccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Eleccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('circuito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.circuito')),
                ('tipo_eleccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.tipoeleccion')),
            ],
        ),
        migrations.AddField(
            model_name='circuito',
            name='seccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.seccion'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('circuitos', models.ManyToManyField(blank=True, to='control.circuito')),
                ('eleccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='control.eleccion')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('num_orden', models.IntegerField()),
                ('dni', models.IntegerField()),
                ('apellido', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('clase', models.IntegerField()),
                ('domicilio', models.CharField(max_length=100)),
                ('voto', models.BooleanField(default=False)),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control.mesa')),
            ],
            options={
                'unique_together': {('dni', 'apellido', 'nombre', 'num_orden')},
            },
        ),
    ]
