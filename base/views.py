from django.shortcuts import render , redirect
from django.http import HttpResponse
from httpx import get
from .models import Room , Topic , Message, User
from .forms import RoomForm , MessageForm , UserForm , MyUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.models import User
# it is mainly imported for login form to check wether user exist or not , we are doing this because we are doing all the work manually

from django.db.models import Q  # for matching different queries using or(|)  or and (&)

# rooms=[
    # {'id':1 , 'name':"Let's learn python!"},
    # {'id':2 , 'name':"Design with me"},
    # {'id':3 , 'name':"Frontend developers"}
# ]
def home(request):
    # q=request.GET.get('q')  # it will return the query set which was passed like in href = "{% url 'home' %}?q"
    
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    ## Here we are using GET so it will only response to GET method not with the queries with POST method 
      
    # it will set q="" if it is None , before it was displaying nothing when q was not defined or q=None   
    # so the url will become like 'http://127.0.0.1:8000' if q not set to anything or q=None
    
    # rooms= Room.objects.all()  # without q / before defining q in home.html
    # rooms= Room.objects.filter(topic=q) # we can't just write like this , it will not work
    # rooms= Room.objects.filter(topic__name=q)  #__name is used to access parent's (Topic) name maybe , just check once
    
    # rooms= Room.objects.filter(topic__name__icontains=q)
    # icontains --> not case sensitive while comparing like a==A --> True
    # contains --> case sensitive  a==A --> False
    
    rooms= Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(host__username__icontains=q))
    
    rooms_count=rooms.count()  # we can use len() method also but count() works much faster than len()
    
    # topics = Topic.objects.all()  # will return all the topics
    
    topics = Topic.objects.all()[0:5]  # will return only 5 topics
    
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q) | Q(user__username__icontains=q))
         # to add in recent activity field
    context = {'rooms':rooms , 'topics':topics,'rooms_count':rooms_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)
    
# def room(request):
def room(request,pk):
    # rooms=Room.objects.all()
    # room=None
    # for i in rooms:
        # if i['id']==int(pk):  # before using model
        # # if i.id==int(pk):   # after using model
            # room=i
            
    # short form to write the above code
    room=Room.objects.get(id=pk)
    # messages=room.message_set.all()  ## room have a child which is Message model so for accessing all the things of Message we write it in lowercase along with set. Syntax --> child_model(in lowercase)_set.all()
    # Give us the set of all details related to Message model
    
    # if we write messages= , then it will write it in flash messages also which will be displayed on the top along with message in conversation . 
    
    # room_messages=room.message_set.all()   # if you are using meta class in Room model
    
    room_messages=room.message_set.all().order_by('-created','-updated') 
    
    # context={'room':room , 'messages':room_messages}
    # here we need to change 'messages' to 'room_messages' because if we don't change it then also it will create the same issue
    
    participants= room.participants.all()
    if request.method=="POST":
        message=Message.objects.create(
            user=request.user ,# request.user is the user who sends the request or who is signed in at that time
            room=room,
            body=request.POST.get('body')  # here we have written 'body' inside get field because we have named the input field 'body' 
        )
        
        room.participants.add(request.user)
        #  it will add the user if the user send message in the room
        
        return redirect('room', pk=room.id)
        # we are writing this because we are sending a POST request , so there are chances that page may give some error or something else , so it is important that the page reloads once. If we use redirect then it will send them to the same location but will reload the page.
        ### if we don't redirect it , it will then also return it to the same page and work as we wanted but it is good to reload the page once .
    
    context={'room':room , 'room_messages':room_messages, 'participants':participants}
    
    
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    room_messages=user.message_set.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    heading="CREATE ROOM"
    button="Create Room"
    
    context={'form':form ,'topics':topics, 'heading':heading , 'button':button}

    
    if request.method=="POST":
        # print(request.POST)
        # will print this in terminal :
            # <QueryDict: {'csrfmiddlewaretoken': ['PFFKqgzcFnhA5yZUgpUUc5JLpyrslO1yG5XqTDmONqHMoVHRd6yg8iDKDezozF3W'], 'host': ['1'], 'topic': ['2'], 'name': ["Let's learn django . "], 'description': ['']}>
            
            # request.POST.get("keyname") here we access value through the key from request.POST
            
            # request.POST.get('name')
    
            # in this way we collect all the data but in django a predefined way is already defined to do this and that is given below --
            
            ''' 
            
            
            form = RoomForm(request.POST)
            
            # it will get all the data of RoomForm and then store it in form .  
            # print(form)  it is printing the form
            
              
            if form.is_valid():
                # form.save()  # before we excluded the 'host' and 'participants' field from the form (can see in forms.py)
                room=form.save(commit=False)
                room.host = request.user     # will set the host to the user who requested to create the room
                
                # participants will be added automatically when the comment on the room
                
                room.save()
                
                return redirect('home') 
                
    
            '''          
            
            # we are using this method because it will be very complicated if try to update to create new topic in the database with the help of modal form , so it is a lot easier method . The above one will work correctly but will not create a topic in database if topic does not exist in topic list or db and user wants to create topic other than mentioned topic in the database
            
            
            topic_name =request.POST.get('topic')
            topic,created=Topic.objects.get_or_create(name=topic_name)
            # it will get the topic if it found in database or topic is present in database otherwise it wil create the topic in the database
            # if topic found then will be stored in topic otherwise will be stored in created
            
            Room.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description')
            )
            return redirect('home')
            
    return render(request,"base/create_room.html",context)
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # form = RoomForm() # it will give a empty form , there mill be no prefilled field like it needs to be in the updation form .
    
    form = RoomForm(instance = room)
    # this form will be prefilled with the values stored in the room 
    
    topics=Topic.objects.all()
    heading="UPDATE ROOM"
    button="Update Room"
    
    context={'form':form , 'topics':topics ,'room':room , 'heading':heading , 'button':button}
    # we are passing room in the context because as we used input field in the create_room field for the topics and set its value="" so it will not be prefilled or prefilled will the value = "" which is empty . So to solve the issue we will use value="{{room.topic.name}}" 
    
    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here</h1>')
        
    if request.method == "POST":
        '''
        form = RoomForm(request.POST , instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
        '''
        
        # we haven't used the form because we want to let user add new topic if it doesn't exist in db, can see more about it in createRoom
        
        topic_name =request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
    
    return render(request , 'base/create_room.html' , context)


def loginView(request):
    # there is predefined function name named login() so we can't use like login(request) , it will create conflict between two
    
    page="Login"
    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method == "POST":
        # username=request.POST.get('username').lower()    # .lower() because at the time of user registration we have converted username into lowercase and saved it to db in lowercase . we have commented this because now we will use email to login , in the place of username
        
        
        email=request.POST.get('email')
        password = request.POST.get('password')
        # in createRoom we have used modal to this work but here we are doing all by ourselves.
        try:
            user= User.objects.get(email=email)
        except:
            # if we are not able to get the user , it will mainly happen because User will not exist in database so in that case we will -
            # messages.add_message(request,messages.ERROR , "User Does Not Exist") # it can also be used but we mainly use a shortcut method
            
            messages.error(request,"User Does Not Exist")
            
        user=authenticate(request,email=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Check Username OR Password")
            
    return render(request,"base/login_register.html",{"page":page})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreationForm()
    page="Sign up"
    
    if request.method=="POST":
        form = MyUserCreationForm(request.POST)  # it will return all the data stored in POST request
        if form.is_valid():
            user=form.save(commit=False)    # it will save the user details and freez the further process and will not save it but it will actually store it in user right a way .
            
            user.username = user.username.lower()  #here it is used for cleaning purpose if we want to save the username all in lowercase but I'll not prefer that .
            
            user.save()  # it will finally save the data into the database after converting the username into lowercase.
            # because of this we also need to use lower() in login -> username = request.POST.get(username).lower()
            
            login(request,user)   # it will logged in user just after the registration and saving the detail in database from the 'user'
            return redirect('home')
        else:
            messages.error(request,"Enter a valid username or password")
    
    return render(request,"base/login_register.html",{"form":form,"page":page})
    
@login_required(login_url='login')
def deleteRoom(request , pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here</h1>')
    if request.method=="POST":
        room.delete()  # to delete that item from the database like save()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required
def deleteUser(request):
    user=request.user
    obj=f"Your Account - {user.username}"
    if request.method == 'POST':
            User.objects.get(id=user.id).delete()
            return redirect('home')
    else :
        return render(request,'base/delete.html',{'obj':obj})

@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    
    
    if request.method == 'POST':
        # form=UserForm(request.POST,instance=user)
        form=UserForm(request.POST,request.FILES,instance=user)
        # we need to add 'request.FILES' so that it can process the file which we get and send the file to the database
        
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    
    return render(request,'base/update_user.html',{'form':form})

@login_required(login_url='login')
def deleteMessage(request , pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('<h1>You are not allowed here</h1>')
    if request.method=="POST":
        message.delete()  # to delete that item from the database like save()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def editMessage(request, pk):
    message = Message.objects.get(id=pk)
    # form = MessageForm() # it will give a empty form , there will be no prefilled field like it needs to be in the updation form .
    
    form = MessageForm(instance= message)
    # this form will be prefilled with the values stored in the room 
    
    if request.user != message.user:
        return HttpResponse('<h1>You are not allowed here</h1>')
    
    if request.method == "POST":
        form = MessageForm(request.POST , instance=message)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request , 'base/update_message.html' ,{'form':form } )




def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    topics=Topic.objects.filter(Q(name__icontains=q))
    context={'topics':topics}
    return render(request,'base/topics.html',context)
    
def activitiesPage(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ""
    activity_messages=Message.objects.filter(Q(room__topic__name__icontains=q) | Q(user__username__icontains=q))
    context={'activity_messages':activity_messages}
    return render(request,'base/activity.html',context)
    