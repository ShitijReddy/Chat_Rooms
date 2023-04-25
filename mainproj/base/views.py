from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from.models import Room, Topic, Message
from .forms import RoomForm, TopicForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from .mixins import GroupRequiredMixin


from django.views import View

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            # pass
            # messages.error(request, 'User does not exist')
            pass
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is Incorrect')
    context = {'page': page}
    return render(request, "base/login_register.html", context)

class LogoutUser(View):
    # group_required = []
    def get(self, request):
        logout(request)
        return redirect("home")


# def registerPage(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'base/login_register.html', {'form': form})

class RegisterPage(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'base/login_register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')


class Home(View):
    def get(self, request):
        print(request.user)
        q = request.GET.get('act') if request.GET.get('act') != None else '5'
        que = request.GET.get('top') if request.GET.get('top') != None else ''
        
        room_messages = Message.objects.all()
        # rooms = Room.objects.all()
        rooms = Room.objects.filter(
            Q(topic__name__icontains = que)
        )
        room_count = rooms.count()
        q = int(q)
            # activity
        room_messages = Message.objects.order_by("-created")[:q]
        topics = Topic.objects.all()
        
        context = {'room_messages':room_messages,'rooms':rooms, 'topics':topics, 'room_count':room_count}
        return render(request, "base/home.html", context)   


class SearchMessages(View):
    def get(self,request):
        q = request.GET.get('que') if request.GET.get('que') != None else ''
        room_messages = Message.objects.filter(Q(body__icontains = q))
        context = {'room_messages':room_messages}
        return render(request, 'base/search_messages.html', context)
    

class RoomView(GroupRequiredMixin, View):
    group_required = [u'viewer_group']
    # permission_required = ('base.view_room', 'base.view_message')
    def get(self, request, pk):
        
        room = Room.objects.get(id = pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()
        context = {'room' :room, 'room_messages': room_messages, 'participants':participants} 
        return render(request, "base/room.html", context)
    
    def post(self, request, pk):
        room = Room.objects.get(id = pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


class RoomSearch(View):
    def get(self, request, pk):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        room = Room.objects.get(id = pk)
        room_messages = Message.objects.filter(room = id).filter(body__icontains = q)
        # room_messages = room.message_set.all()
        participants = room.participants.all()
        context = {'room' :room, 'room_messages': room_messages, 'participants':participants} 
        return render(request, "base/room.html", context)
    
    def post(self, request, pk):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        room = Room.objects.get(id = pk)
        room_messages = Message.objects.filter(room = id).filter(body__icontains = q)
        # room_messages = room.message_set.all()
        participants = room.participants.all()
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


class UserProfile(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        #   REVERSE RELATION
        room_messages = user.message_set.all()
        rooms = user.room_set.all()
        topics = Topic.objects.all()
        context = {'room_messages': room_messages,'user':user, 'rooms':rooms, 'topics':topics}
        return render(request,'base/profile.html', context)


class CreateRoom(GroupRequiredMixin, View):
    group_required = [u'creator_group']

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("You should be logged in")
        form = RoomForm()
        return render(request, 'base/room_form.html', {'form':form})
    
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("You should be logged in")
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else :
            return render(request, 'base/room_form.html', {'form':form})

class CreateTopic(GroupRequiredMixin, View):
    group_required = [u'admin_group']

    def get(self, request):
        form = TopicForm()
        return render(request, 'base/room_form.html', {'form':form})
    
    def post(self, request):
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else :
            return render(request, 'base/room_form.html', {'form':form})

class UpdateRoom(GroupRequiredMixin, View):

    group_required = [u'creator_group']

    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)

        if request.user != room.host:
            return HttpResponse("Sorry, You Can't Update as you are NOT THE HOST of this room")
        return render(request, 'base/room_form.html', {'form':form})
    
    # @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)

        if request.user != room.host:
            return HttpResponse("Sorry, You Can't Update as you are NOT THE HOST of this room")
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'base/room_form.html', {'form':form})


class DeleteRoom(GroupRequiredMixin, View):
    group_required = [u'creator_group']

    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        if request.user != room.host:
            return HttpResponse("Sorry, You Can't DELETE as you are NOT THE HOST of this room")
        return render(request,'base/delete.html', {'obj': room})
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        if request.user != room.host:
            return HttpResponse("Sorry, You Can't DELETE as you are NOT THE HOST of this room")
        room.delete()
        return redirect('home')


class Search(View):
    def get(self, request):
        query =request.GET['query']
        rooms = Room.objects.filter(name__icontains = query)
        context = {'rooms': rooms}
        # query = request.GET
        return render(request, 'base/search.html', context)


class SearchUser(View):
    def get(self, request):
        queryUser =request.GET['query']
        rooms = Room.objects.filter(host__username__icontains = queryUser)
        context = {'rooms': rooms}
        # query = request.GET
        return render(request, 'base/search-user.html', context)


class DeleteMessage(GroupRequiredMixin, View):
    # permission_required = ('base.delete_message', 'base.view_message')
    group_required = [u'viewer_group']

    def get(self, request, pk):
        message = Message.objects.get(id=pk)
        if request.user != message.user:
            return HttpResponse("Sorry, You Can't DELETE as you are NOT THE HOST of this message")
        return render(request,'base/delete.html', {'obj': message})

    def post(self, request, pk):
        message = Message.objects.get(id=pk)
        room = message.room
        if request.user != message.user:
            return HttpResponse("Sorry, You Can't DELETE as you are NOT THE HOST of this message")
        message.delete()
        return redirect('room', pk=room.id)
#     context = {'room' :room, 'room_messages': room_messages, 'participants':participants} 
#     return render(request, "base/room.html", context)


class UpvoteMessage(GroupRequiredMixin, View):
    # permission_required = ('base.change_message', 'base.view_message')
    group_required = [u'viewer_group']

    def get(self, request, pk):
        message = Message.objects.get(id=pk)
        room = message.room
        if request.user == message.user:
            return HttpResponse("You can't upvote your own message")

        message.votes += 1
        message.save()

        return redirect('room', pk=room.id)