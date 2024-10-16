from django.db import models
from person.models import Authors
from library_structure.models import Shelf


class EditionKinds(models.Model):
    edition_type = models.CharField(max_length=50)

    class Meta:
        db_table = "EditionKinds"
        verbose_name = "Виды изданий"

    def __str__(self):
        return self.edition_type


class Books(models.Model):
    name = models.CharField(max_length=50)
    author = models.ManyToManyField(Authors, related_name="books")
    edition_kind = models.ForeignKey(EditionKinds, on_delete=models.CASCADE)
    book_number = models.CharField(max_length=10, unique=True)
    pages_count = models.IntegerField()
    edition_date = models.DateField()
    note = models.TextField(blank=True, null=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, null=True, unique=True)

    class Meta:
        db_table = "Books"
        verbose_name = "Книги"

    def __str__(self):
        return self.name+' '+self.book_number
