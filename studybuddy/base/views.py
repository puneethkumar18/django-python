from django.shortcuts import render,redirect 
from django.http import HttpResponse 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'FrontEnd Developer!'},
# ]

def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

        except:
            messages.error(request,'User doest not exits!!')
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
             login(request,user)
             return redirect('home')
        else:
            messages.error(request,'UserName OR Password dos not exist !')
    
    context = {"page":page} 
            
    return render(request,'base/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = "register"
    form = MyUserCreationForm()
    if request.method == "POST":
        form  = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occured during registation")

    context = {"page":page,"form":form}
    return render(request,'base/login.html',context)

def home(request):
    if request.user.is_authenticated == False:
        return render(request,'base/login.html')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms  = Room.objects.filter(
        Q(topic__name__icontains = q)| 
        Q(name__icontains = q)|
        Q(host__username__icontains = q)|
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()[0:4]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q)|
        Q(user__username__icontains=q)|
        Q(room__topic__name__icontains=q)
        )
    context = {
        "rooms":rooms,
        "topics":topics,
        "rooms_count":rooms_count,
        'room_messages':room_messages
        }
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id = pk)
    comments = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            description = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'comments':comments,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user':user,
        'rooms':rooms,
        'room_messages':room_messages,
        'topics':topics
        }
    return render(request,'base/profile.html',context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect("home")
    context = {'form':form,'topics':topics}
    return render(request,"base/create-room.html",context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are to allowed to update in this rooom !!')
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url="login")
def deleteMessage(request,pk):
    message  = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Your not allowed to delete this Message")
    if request.method == "POST":
        message.delete()
        room = message.room
        room.participants.remove(message.user)
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    userForm = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    return render(request,'base/update-user.html',{'userForm':userForm})


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {"room_messages":room_messages}
    return render(request,'base/activity.html',context)



def errorpage(request,exception):
    return render(request,'base/404Error.html',status=404)