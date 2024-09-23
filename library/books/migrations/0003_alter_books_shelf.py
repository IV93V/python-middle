# Generated by Django 4.2.14 on 2024-09-22 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_structure', '0001_initial'),
        ('books', '0002_alter_books_shelf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='shelf',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library_structure.shelf', unique=True),
        ),
    ]