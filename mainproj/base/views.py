from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from.models import Room, Topic, Message, Pizza, Topping, Restaurant
from .forms import RoomForm, TopicForm, UserProfileForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch


from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from .mixins import GroupRequiredMixin
from .query_debugger import query_debugger

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
    # @query_debugger
    @method_decorator(query_debugger, name='dispatch')
    def get(self, request):
        # return HttpResponse("Welcome to Home Page")
        print(request.user)
        q = request.GET.get('act') if request.GET.get('act') != None else '5'
        que = request.GET.get('top') if request.GET.get('top') != None else ''
        
        # room_messages = Message.objects.all()
        # rooms = Room.objects.all()
        rooms = Room.objects.filter(
            Q(topic__name__icontains = que)
        )

        # rooms = Room.objects.all()
        # rooms = Room.objects.select_related('topic','host').all()
        # room_array = []
        # for room in rooms:
        #     room_array.append({'host':room.host, 'name':room.name, 'topic':room.topic.name})
        # print(room_array)

        
        


        # rooms = Room.objects.select_related('topic')

        # rooms = Room.objects.select_related('topic').filter(
        #     Q(topic__name__icontains = que)
        # )
        room_count = rooms.count()
        q = int(q)
        
        # # activity
        #               ONLY 
        room_messages = Message.objects.only('created', 'body').order_by("-created")[:q]
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
    @method_decorator(query_debugger, name='dispatch')
    def get(self, request, pk):
        #       DEFER Method
        room = Room.objects.defer('updated', 'created').get(id = pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()
        context = {'room' :room, 'room_messages': room_messages, 'participants':participants} 

        # queryset = Room.objects.all()
        # queryset = Room.objects.prefetch_related('participants')
        # rooms = []
        # for room in queryset:
        #     particpants = room.participants.all()
        #     rooms.append({'name':room.name, 'participants':particpants})
        # print(rooms)

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

class PizzaShop(View):
    def get(self, request):
        # queryset = Restaurant.objects.all()
        query = Pizza.objects.prefetch_related(Prefetch('toppings', queryset=Topping.objects.order_by('-name')))
        pizzas = []
        for pizza in query:
            toppings = pizza.toppings.all()
            pizzas.append({'name':pizza.name, 'toppings':toppings})
        # print(pizzas)
        context = {'pizzas':pizzas}
        return render(request,"base/pizza_shop.html", context)

    def post(self, request):
        pass

class RestaurantView(View):
    def get(self, request):
        queryset = Pizza.objects.only('name', 'origin')
        restaurants = Restaurant.objects.prefetch_related(Prefetch("best_pizza", queryset))
        for rest in restaurants:
            print("rest name:", rest.name)
            print("Best Pizza:" ,rest.best_pizza)
            print("Origin:", rest.best_pizza.origin)
        #     print("Toppings are:")
            # for topping in rest.best_pizza.toppings.all():
            #     print("  ",topping)
            # print("\n")

        # print(queryset__pizzas__toppings)
        # print(queryset)

        rests = []
        for rest in restaurants:
            best_pizza = rest.best_pizza
        #     toppings = pizzas__toppings.all()
            rests.append({'name':rest.name, 'best_pizza':best_pizza})
        # print(rests)
        context = {'rests':rests}
        return render(request,"base/restaurant.html", context)
        # return redirect('home')

    def post(self, request):
        pass

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
        
class CreateUser(GroupRequiredMixin, View):
    group_required = [u'admin_group']

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'base/room_form.html', {'form':form})
        # return redirect('home')
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'base/room_form.html', {'form':form})
        
class EditUserProfile(GroupRequiredMixin, View):
    group_required = [u'admin_group']

    def get(self, request):
        form = UserProfileForm()
        return render(request, 'base/room_form.html', {'form':form})
    
    def post(self, request):
        form = UserProfileForm(request.POST)
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
        room = Room.objects.only('id').get(id=pk)
        if request.user != room.host:
            return HttpResponse("Sorry, You Can't DELETE as you are NOT THE HOST of this room")
        return render(request,'base/delete.html', {'obj': room})
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        room = Room.objects.only('id').get(id=pk)
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