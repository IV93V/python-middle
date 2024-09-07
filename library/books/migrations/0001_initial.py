# Generated by Django 4.2.14 on 2024-09-07 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library_structure', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditionKinds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edition_type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Виды изданий',
                'db_table': 'EditionKinds',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('book_number', models.CharField(max_length=10, unique=True)),
                ('pages_count', models.IntegerField()),
                ('edition_date', models.DateField()),
                ('Note', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='person.authors')),
                ('edition_kind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.editionkinds')),
                ('shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_structure.shelf')),
            ],
            options={
                'verbose_name': 'Книги',
                'db_table': 'Books',
            },
        ),
    ]