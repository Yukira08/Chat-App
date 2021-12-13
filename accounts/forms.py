from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    #username=forms.username(help_text="Required. Make it unique")
    class Meta(UserCreationForm.Meta):
        help_texts={
        'username':None,
    }
        fields = UserCreationForm.Meta.fields + ("email",)
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None