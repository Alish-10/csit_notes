from datetime import datetime
from email.policy import default
from operator import mod
from statistics import mode
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


    
# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, default="")
    description = models.TextField()
    
    '''
    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"
    '''

    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Material(models.Model):
    title=models.CharField(max_length=70)
    categorise=models.CharField(max_length=70)
    image=models.ImageField(upload_to="static/images")
    content=RichTextField(blank=True,null=True)


    
    def __str__(self):
        return str(self.pk)

    
    def clean(self):
        self.categorise = self.categorise.upper()
        self.title = self.title.capitalize()

class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    material=models.ForeignKey(Material,on_delete=models.CASCADE,default=None)
    rating=models.CharField(max_length=70)
    rated_date=models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    fname = models.CharField(max_length=10)
    lname=models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    subject = models.TextField()


    def __str__(self):
        return self.fname+self.lname


class Member(models.Model):
    name=models.CharField(max_length=30)
    dob=models.DateField(default=datetime.date.today)
    email = models.EmailField()
    image=models.ImageField(upload_to="static/images", default=1)
    bio = RichTextField(blank=True,null=True)

    def __str__(self):
        return self.name