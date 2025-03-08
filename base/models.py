from importlib.metadata import requires
from typing import Required
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser) :
    full_name=models.CharField(max_length=250,null=True)   # with null=True , we can store null value but can not leave it blank
    username = models.CharField(max_length=200 , unique=True,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True,blank=True)   

    avatar = models.ImageField(null=True , default='avatar.svg')
    
    USERNAME_FIELD = 'email'        # Users log in with email.
    REQUIRED_FIELDS = ['username']      # Username is still required during registration.
    
    def __str__(self):
        return self.username  # Ensures username is returned instead of email
        # __str__ method returns self.username, preventing email from being shown instead.
        
    ''' When USERNAME_FIELD = 'email', Django’s authentication system expects the email for login.
        If you print request.user in the frontend, it might show the email because Django’s default __str__ method might be using USERNAME_FIELD.
        Explicitly defining __str__ to return self.username fixes this issue. '''


class Topic(models.Model):
    name= models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    
    # topic = models.OneToOneField("Topic", on_delete=models.SET_NULL) # SET_NULL will set the topic field to NULL in database if Parent topic is deleted or topic gets deleted from Topic Model
    # base.Room.topic: (fields.E320) Field specifies on_delete=SET_NULL, but cannot be null.
        # HINT: Set null=True argument on the field, or change the on_delete rule.
        # It is saying that if you want to set the field to null after deletion make null=True because by default null=False
    
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True) # SET_NULL will set the topic field to NULL in database if Parent topic is deleted or topic gets deleted from Topic Model
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank= True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)  # null=True , null has no effect on many to many
    # we have given the related name because it was creating a clash between host and participants because both have relation to User because of that we need to specify related name . We can give any name we want to give .
    
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    
    # foreign_key() establish ManytoOne relationship ,one topic can have different rooms but one room can have only one topic 
    
    class Meta :
        ordering = ['-created']
        # it will arrange the room list in decending order -> newest at the top and oldest at the bottom
        
        # ordering = ['updated', 'created']
        # it will arrange the room in ascending order , newest at the bottom and oldest at the top
    
    def __str__(self):
        return self.name
    
class Message(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)
    
    # class Meta :
        # ordering = ['-updated', '-created']
    def __str__(self):
        return self.body[0:50]
        # body[0:50] will slice down the message into message of 50 words only , it can be shown as preview
        
