from django.db import models

class Agents (models.Model):
    SEX_CHOICE = (
        (0, 'Женский'),
        (1, 'Мужской'),
    )
    surname = models.CharField(max_length =30)
    firstname = models.CharField(max_length =30)
    lastname = models.CharField(max_length =30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICE)

    class Meta:
        db_table = 'Agents'
        verbose_name = 'Контрагенты'


class Authors (models.Model):
    pid = models.ForeignKey(Agents, on_delete = models.CASCADE, unique=True)
    rating = models.FloatField()

    class Meta:
        db_table = 'Authors'
        verbose_name = 'Авторы'


class Librariers (models.Model):
    agent = models.ForeignKey(Agents, on_delete = models.CASCADE)
    employment_date = models.DateField()
    dismiss_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Librariers'
        verbose_name = 'Библиотекари'