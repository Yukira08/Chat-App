from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    #username=forms.username(help_text="Required. Make it unique")
    class Meta(UserCreationForm.Meta):
        help_texts={
        'username':None
    }
        fields = UserCreationForm.Meta.fields + ("email",)