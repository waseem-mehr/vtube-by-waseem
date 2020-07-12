from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Video,UserModel
from django import forms
from django.forms import ModelForm

class VideoForm(ModelForm):
    class Meta:
        model=Video
        fields=['title','categorey','thumbnail','video']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'categorey':forms.Select(attrs={'class':'form-control'}),


        }
        help_texts={
            'video':'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***The video not more than 15 seconds long'
        }
        error_messages={}
        labels={
            'title':'Enter the title of the video :',
            'categorey':'Select the category ',
            'thumbnail':'Select the thumbnail ',
            'video':'Select the video ',
        }
class ImageForm(ModelForm):
    class Meta:
        model=UserModel
        forms=['image']
        exclude=['user']
        labels={
            'image':'please select profile image'
        }


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ['username','password1','password2']
        model = get_user_model()
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),

        }



