from dataclasses import fields
from django.forms import ModelForm 
from .models import Message, Room, User
# from django.contrib.auth.models import User   # we have commented this because now the User model is in base app
from django.contrib.auth.forms import UserCreationForm



# they are inheriting ModelForm and other type of predefined forms if you notice


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name','username','email','password1','password2']

class RoomForm(ModelForm):
    
    class Meta :
        model=Room
        fields='__all__'
        # this will add all the fields which needs input from Room model
        
        # fields = ['name' , 'topic', ...]
        #  can add fields like this also if we want only few fields
        
        exclude=['host','participants']
        # want to exclude these fields in the form so that it can not be visible to the user
        
class MessageForm(ModelForm):
    class Meta:
        model=Message
        fields=('body',)
        
class UserForm(ModelForm):
    class Meta:
        model = User
        
        fields=['avatar','full_name','username','email','bio']
        
        
        # fields=['username','first_name','last_name','email']
        # User model have the fields we see when we go to user -> user's profile in it . like is_staff , is_active etc
        
        # if you want to see all the fields of user , you can set fields = '__all__'
        
