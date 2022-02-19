from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=120)
    logo=models.ImageField(upload_to='customers/%Y%m', default='customers/No_image.png' )
    def __str__(self) :
        return str(self.name)