from django import forms

from .models import Project, Entry

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['text']
        labels = {'text' : ''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text' : 'Entry:'}
        widgets ={'text' : forms.Textarea(attrs={'cols' : 80})}