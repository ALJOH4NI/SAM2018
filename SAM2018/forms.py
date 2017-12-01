from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from .models import Paper, Review, Deadlines


class Signupform(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username','email','password1','password2', 'last_name','first_name'
        )

class UplaodFile(forms.ModelForm):

    class Meta:
        model = Paper
        fields = (
            'title','version','uplaod','authorName','contact'
        )


class AssignForm(forms.Form):
    class Meta:
        model = Review
        fields = (
            'paper_id','pcm_id'
        )

class DeadlineForm(forms.Form):
    class Meta:
        model = Deadlines
        fields = (
            'date','group'
        )
