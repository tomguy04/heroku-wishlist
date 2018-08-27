# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["password1"] = "password must be at least 8 characters"

        if 'name' in postData:
            if len(postData['name']) < 3:
                errors["name"] = "name must be at least 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "username must be at least 3 characters"
        if 'datehired' in postData:
            if len(postData['datehired']) < 1:
                errors["password"] = "please enter your hire date"

        return errors

class ItemManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
                errors["name"] = "Item/Product in blank, please add an Item/Product"
        else:
            if len(postData['name']) < 4:
                errors["name"] = "Item/Product must be at least 4 characters long"

        return errors
        
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
         return self.name

class ItemList(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name = 'users') #added, a user can have many tripscheudles.
    objects = ItemManager()

class Follow(models.Model): 
    item = models.ForeignKey(ItemList, related_name = 'users')
    follower= models.ForeignKey(User, related_name = 'items')
