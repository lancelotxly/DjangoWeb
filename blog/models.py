from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    publish_date = models.DateField()
    publisher = models.ForeignKey("Publisher",on_delete=models.CASCADE,related_name='books')
    author = models.ManyToManyField('Author')
    fk = models.OneToOneField
    def __str__(self):
        return self.title

class Publisher(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Test(models.Model):
    img = models.ImageField(upload_to='blog/static/')
    title = models.CharField(max_length=20)


