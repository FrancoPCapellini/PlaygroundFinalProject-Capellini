from audioop import reverse
from django.shortcuts import render, redirect 
from .models import Topic, Entry, Book
from .forms import TopicForm , EntryForm, BookForm, BookFinderForm, UserCreationFormCustom # redirect y TopicForm se agregan con los forms, despues de crear forms.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Para el login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
def index(request):
    """ The home page for Learning Log. """
    return render(request, "learning_logs/index.html")

@login_required
def topics(request):
    """ Show all topics. """
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {'topics': topics}
    """
    A context is a dictionary in which the keys are names we'll use in the template to access 
    the data, and the values are the data we need to send to the template.
    """
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id): # accepts the value captured by the expression /<int:topic_id>/ .
    """ Show a single topic and all its entries. """
    # topic and entries are queries, for check if this is ok, test it in Django shell
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    
    if topic.owner != request.user:
        raise Http404
    
    context = {'topic':topic , 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ Add a new topic. """
    # GET request is used for pages that only reed data from the server.
    # POST request when the user need to submit information through a form. 
    """
    The new_topic() function takes in the request object as a parameter. 
    When the user initially requests this page, their browser will send a GET request.
    Once the user has filled out and submitted the form, their browser will submit a POST request.
    Depending on the request, we'll know whether the user is requesting a blank form
    (a GET request) or asking us to process a completed form (a POST request).  
    """
    if request.method != 'POST': # The request method is a GET or POST, in this case we want its diferent than POST
        # No data submitted; create a blank form. 
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data = request.POST)
        if form.is_valid():              
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()    
            return redirect('learning_logs:topics') 
            # redirect is used to redirect the user back to the topics page after they submit their topic

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ Add a new entry for a particular topic. """
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        # NO data submitted; create a blank form. 
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data = request.POST) # We process the data by making an instance of EntryForm, populated with the POST data from the request object
        if form.is_valid():
            new_entry = form.save(commit = False) #  the argument commit=False to tell Django to create 
                                                  # a new entry object and assign it to new_entry without saving it to the database yet.
            new_entry.topic = topic # We set the topic attribute of new_entry to the topic we pulled from the database, at beginning. 
            new_entry.save()
            return redirect('learning_logs:topic', topic_id = topic_id) # this view renders the topic page and the user should see their new entry.
    
    # Display a blank or invalid form.
    context = {"topic":topic, "form":form}
    return render(request, 'learning_logs/new_entry.html', context) # This code will execute for a blank form or for a submitted form that is evaluated as invalid

@login_required
def edit_entry(request, entry_id):
    """ Edit an existing entry. """
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance = entry) # This tells django to create the form prefilled with info form the existing entry object.
    else:
        # POST data submitted; process data. 
        form = EntryForm(instance = entry, data = request.POST) # Create a form instance based on the info associated with the existing entry object, updated with data from request.POST
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

def BookFinder(request):
    """ search for the book you read """
    if request.method == 'GET':
        form = BookFinderForm(data = request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            books = Book.objects.filter(name__icontains=name, owner=request.user)
            context = {'name': name,'books': books}
            return render(request, 'learning_logs/CBV/book_list.html', context)
    else:
        form = BookFinderForm()
    
    context = {'form': form}
    return render(request, 'learning_logs/CBV/book_list.html', context)

# def NewBook(request):
#     """ add a new particular book """
#     if request.method != 'POST':
#         form = BookForm()
#     else:
#         form = BookForm(data = request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect ('learning_logs:BookFinder')
    
#     context = {'form':form}
#     return render(request, 'learning_logs/new_book.html', context)

# def AllBooks(request):
#     list_books = Book.objects.all()
#     context = {'books':list_books}
#     return render(request, "learning_logs/all_books.html", context)

# def DeleteBook(request, book_name):
#     book = Book.objects.get(name = book_name)
#     book.delete()

#     list_books = Book.objects.all()
#     context = {'books':list_books}
#     return render(request, "learning_logs/all_books.html", context)
    
# def EditBook(request, book_name):
#     book = Book.objects.get(name = book_name)

#     if request.method != 'POST': 
#         form = BookForm(instance = book) 
#     else:
#         form = BookForm(instance = book, data = request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('learning_logs:AllBooks')
    
#     context = {'book': book, 'form': form}
#     return render(request, 'learning_logs/edit_book.html', context)

#CBV
class BookListView(LoginRequiredMixin, ListView):
    model = Book # modelo con el que vamos a trabajar
    context_object_name = 'books' # nos permite pasarle al template como queremos llamar al conjunto de datos
    template_name = 'learning_logs/CBV/book_list.html'
    
    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'learning_logs/CBV/book_details.html'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'learning_logs/CBV/book_create.html'
    fields = ['name','author','description'] # lista con los campos que se renderizen en el formulario

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('learning_logs:ListBooks') # nombre de la vista donde nos va a redirigir una vez hagamos submit 

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'learning_logs/CBV/book_edit.html'
    fields = ['name','author','description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('learning_logs:ListBooks')
    

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'learning_logs/CBV/book_delete.html'
    fields = ['name','author','description']
    success_url = reverse_lazy('learning_logs:ListBooks')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Check if the user is the owner of the book before deleting
        if self.object.user == self.request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return render(success_url)
        else:
            # Handle unauthorized delete attempt
            return render("You don't have permission to delete this book.")
# -------------------  Login  ---------------------------
# def LoginRequest(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data = request.POST)

#         if form.is_valid():
#             usuario = form.cleaned_data.get('username')
#             contrasenia = form.cleaned_data.get('password')

#             user = authenticate(username = usuario, password = contrasenia)
#             login(request, user)

#             return render(request, 'learning_logs/index.html', {'mensaje': f'Bienvenido {user.username}'})
        
#     else:
#         form = AuthenticationForm()
#         context = {'form':form}
#         return render(request, 'learning_logs/users/login.html', context)

# # -----------------  Registro  ---------------------------
# def Register(request):
#     if request.method == 'POST':
#         form = UserCreationFormCustom(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             form.save()
#             return render(request, 'learning_logs/index.html', {'mensaje':'Usuario Creado :)'})
    
#     else:
#         form = UserCreationFormCustom()
#         context = {'form': form}
#         return render(request, 'learning_logs/users/register.html', context)


