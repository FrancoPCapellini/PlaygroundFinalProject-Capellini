from django import forms
from .models import Topic, Entry, Book # Model we'll work with 

# login
from django.contrib.auth.forms import UserCreationForm, UserModel

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
        widgets = {'description': forms.Textarea(attrs={'cols': 40})}

class BookFinderForm(forms.Form):
    name = forms.CharField(label = 'Search for book', max_length=100)
    author = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=500, required=False)

class UserCreationFormCustom(UserCreationForm):
    username = forms.CharField(label = 'Usuario')
    email = forms.EmailField()
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Repetir contraseña', widget = forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        #saca los mensajes de ayuda
        help_texts = {k:"" for k in fields}
