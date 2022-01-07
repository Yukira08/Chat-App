<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email',)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['img']
=======
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import User
# class CustomUserCreationForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('username','email',)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['image']
        # widgets={
        #     'image': 
        # }


class CustomUserCreationForm(UserCreationForm):
    #username=forms.username(help_text="Required. Make it unique")
    class Meta(UserCreationForm.Meta):
        model = User
        help_texts={
        'username':None,
    }
        fields = UserCreationForm.Meta.fields + ("email",)
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
>>>>>>> beanstalk
