from django import forms
from .models import Eleitor

class LoginForm(forms.ModelForm):
    class Meta:
        model = Eleitor
        fields = ['cpf', 'dataN']