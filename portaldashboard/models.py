from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Note(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.title


class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100)
    title=models.CharField(max_length=200)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Course(models.Model):
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    question=models.CharField(max_length=100)
    answer=models.IntegerField()
    desc=models.CharField(max_length=500)
    opt_one=models.CharField(max_length=100)
    opt_two=models.CharField(max_length=100)
    opt_three=models.CharField(max_length=100,blank=True)
    opt_four=models.CharField(max_length=100,blank=True)
    
  

    def __str__(self):
        return self.question



