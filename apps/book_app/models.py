from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email=postData["email"])
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must be entered and should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must be entered and should be at least 2 characters"
        if not EMAIL_REGEX.match(postData["email"]): 
            errors["email"] = "Not a valid email address" 
        if len(check_email) > 0: 
            errors["email"] = "This email address already exists in the system" 
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be more than 8 characters"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match"
        return errors

    def user_validator(self, postData):
        errors = {}
        check_email = User.objects.filter(email=postData["email"])
        if not EMAIL_REGEX.match(postData["email"]): 
            errors["email"] = "Not a valid email address" 
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be more than 8 characters"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 1: 
            errors["title"] = "Title is required"
        if len(postData["description"]) < 5: 
            errors["description"] = "Description section must contain more than 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


