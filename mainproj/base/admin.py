from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, Pizza, Topping, Restaurant

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Restaurant)
