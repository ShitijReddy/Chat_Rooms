from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group
from .models import Room, Topic

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileForm(ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'group']