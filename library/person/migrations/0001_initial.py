# Generated by Django 4.2.14 on 2024-09-07 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('birth_date', models.DateField()),
                ('sex', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Контрагенты',
                'db_table': 'Agents',
            },
        ),
        migrations.CreateModel(
            name='Libraries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employment_date', models.DateField()),
                ('dismiss_date', models.DateField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.agents')),
            ],
            options={
                'verbose_name': 'Библиотекари',
                'db_table': 'Libraries',
            },
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.agents', unique=True)),
            ],
            options={
                'verbose_name': 'Авторы',
                'db_table': 'Authors',
            },
        ),
    ]
