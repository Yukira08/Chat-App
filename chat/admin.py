from django.contrib import admin
from django import forms
# Register your models here.
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class YourModelForm(forms.ModelForm):
    short_text = forms.CharField(widget=EmojiPickerTextInputAdmin)
    long_text = forms.CharField(widget=EmojiPickerTextareaAdmin)