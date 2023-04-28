from django.db import models
from django.contrib.auth.models import User, AbstractUser

# class User(AbstractUser):
#     points = models.IntegerField(default=0)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #               New field
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    img = models.ImageField(null=True, blank=True, upload_to="images/")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    img = models.ImageField(null=True, blank=True, default='upvote.png')

    class Meta():
        ordering = ['-updated', '-created']


    def __str__(self):
        return self.body[0:55]

class UserContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    roomsCreated = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.user.username



class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    origin = models.CharField(max_length=50, default="Italy")
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50, default="Restaurant Name")
    pizzas = models.ManyToManyField(Pizza, related_name="restaurants")
    best_pizza = models.ForeignKey(
        Pizza, related_name="championed_by", on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name


