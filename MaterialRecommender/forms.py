from django import forms
from django.contrib.auth.models import User
from matplotlib.pyplot import title
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from dataclasses import fields
from logging import PlaceHolder
from matplotlib import widgets

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','category','description']

class DateInput(forms.DateInput):
    input_type = 'date'


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=50, label='Enter your search here......')


class AddMaterialForm(forms.ModelForm):
    class Meta:
        model=Material
        fields='__all__'
        labels={'title':'Title','categorise':'Categorise','image':'Image','content':'Content'}
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'categorise':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}), 
            'content':forms.Textarea(attrs={'class':'form-control'}), 
        }
class MemberForm(forms.ModelForm):
    class Meta:
        model=Member
        fields='__all__'
        labels={'name':'Name','dob':'Date Of Birth','email':'Email','image':'Image','bio':'Bio'}
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'dob':forms.DateInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}), 
            'image':forms.FileInput(attrs={'class':'form-control'}), 
            'bio':forms.Textarea(attrs={'class':'form-control'}), 
        }



class AddRatingForm(forms.ModelForm):
  
    class Meta:
        model=Rating
        fields=['rating']
        labels={'rating':'Rating'}
        widgets={
            'rating':forms.TextInput(attrs={'type':'range','step':'1','min':'1','max':'5','class':{'custom-range','border-1'}})
        }
