from django import forms

class Myform(forms.Form):
    drive_link = forms.URLField(widget=forms.TextInput(attrs={'placeholder': 'Paste your google drive folder link here'}))