from django import forms
from .models import Topic, Entry, Book # Model we'll work with 

class TopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic 
        fields = ['text'] 
        labels = {'text': ''} 

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} 
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','author','description']
        labels = {'name': 'name of the book', 'author': 'author', 'description': 'description'}
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}

class BookFinderForm(forms.Form):
    name = forms.CharField(label = 'Search for book', max_length=100)
    author = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=500, required=False)