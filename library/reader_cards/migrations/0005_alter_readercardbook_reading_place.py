# Generated by Django 4.2.14 on 2024-09-22 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader_cards', '0004_rename_books_id_readercardbook_book_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readercardbook',
            name='reading_place',
            field=models.SmallIntegerField(choices=[(1, 'На руки'), (2, 'Для чтения в зале')]),
        ),
    ]