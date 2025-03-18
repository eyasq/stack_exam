from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def registery_validator(self, postData):
        errors = {}
        first_name = postData.get('first_name')
        if not first_name:
            errors['first_name'] = 'First Name is a required Field!'
        elif len(first_name) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters.'
        elif len(first_name) > 32:
            errors['first_name'] = 'First name can be 32 characters at max'
        last_name = postData.get('last_name')
        if not last_name:
            errors['last_name'] = 'Last Name is a required Field!'
        elif len(last_name) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters.'
        elif len(last_name) > 32:
            errors['last_name'] = 'Last name can be 32 characters at max'
        email = postData.get('email')
        if not email:
            errors['email'] = 'Email is a required Field!'
        elif email and self.filter(email = email).exists():
            errors['email'] = 'Email already exists!'
        elif len(email) < 5:
            errors['email'] = 'Email must be at least 5 characters.'
        password = postData.get('password')
        if not password:
            errors['password'] = 'Password is a required Field!'
        elif len(password) < 8:
            errors['password'] = 'Password must be 8 chars atleast'
        confirm_pw = postData.get('confirm_pw')
        if confirm_pw != password:
            errors['confirm_pw']= "Passwords do not match!"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        email = postData.get('email')
        if not email:
            errors['email'] = 'Email cannot be empty'
        password = postData.get('password')
        if not password:
            errors['password'] = 'Password cannot be empty'
    

class PieManager(models.Manager):
    def pie_validator(self, postData):
        errors = {}
        pie_name = postData.get('pie_name')
        if not pie_name:
            errors['pie_name'] = 'Pie Name is a required Field!'
        elif len(pie_name) < 2:
            errors['pie_name'] = 'Pie Name must be at least 2 characters.'
        elif len(pie_name) > 32:
            errors['pie_name'] = 'Pie Name can be 32 characters at max'
        elif pie_name and self.filter(name = pie_name).exists():
            errors['pie_name'] = 'Pie Name must be unique! There is already a pie with this name.'
        pie_filling = postData.get('pie_filling')
        if not pie_filling:
            errors['pie_filling'] = 'Pie Filling is a required Field!'
        elif len(pie_filling) < 2:
            errors['pie_filling'] = 'Pie Filling must be at least 2 characters.'
        elif len(pie_filling) > 32:
            errors['pie_filling'] = 'Pie Filling can be 32 characters at max'
        pie_crust = postData.get('pie_crust')
        if not pie_crust:
            errors['pie_crust'] = 'Pie Crust is a required Field!'
        elif len(pie_crust) < 2:
            errors['pie_crust'] = 'Pie Crust must be at least 2 characters.'
        elif len(pie_crust) > 32:
            errors['pie_crust'] = 'Pie Crust can be 32 characters at max'
        return errors
   
    


class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Pie(models.Model):
    name = models.CharField(max_length=32)
    filling = models.CharField(max_length=32)
    crust = models.CharField(max_length=32)
    votes = models.IntegerField(default = 0)
    desc = models.TextField(default='A really yummy pie. Highly Recoomended')
    user = models.ForeignKey(User, related_name='pies', on_delete=models.CASCADE)
    voters = models.ManyToManyField(User, related_name='voted_pies', through='Vote')
    objects = PieManager()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pie = models.ForeignKey(Pie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'pie')  