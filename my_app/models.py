from django.db import models
import re
import bcrypt 

# Create Model Manger 
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        user_in_db = User.objects.filter(email=postData['email'])
        if len(postData['username']) < 8:
            errors['username'] = "Hey, your username need to have more than 8 characters"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-z]+$'
        )
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        if len(postData['password']) < 8:
            errors['password'] = "Hey, your password need to have more than 8 characters"
        if postData['password'] != postData['pwd_confirm']:
            errors['password'] = "Passwords must match"


        if user_in_db:
            errors['email'] = "User already exists"
        return errors 
    
    def login_validator(self, postData ):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            login_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), login_user.password.encode()):
                errors['password'] = "Invalid login"
        else:
            errors['password'] = "Invalid login"
        return errors 

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birthday = models.DateField()
    password = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()