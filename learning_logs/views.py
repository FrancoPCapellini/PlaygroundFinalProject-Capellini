from django.shortcuts import render, redirect 
from .models import Topic, Entry, Book
from .forms import TopicForm , EntryForm, BookForm, BookFinderForm# redirect y TopicForm se agregan con los forms, despues de crear forms.py

# Create your views here.
def index(request):
    """ The home page for Learning Log. """
    return render(request, "learning_logs/index.html")

def topics(request):
    """ Show all topics. """
    topics = Topic.objects.order_by("date_added")
    context = {'topics': topics}
    """
    A context is a dictionary in which the keys are names we'll use in the template to access 
    the data, and the values are the data we need to send to the template.
    """
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id): # accepts the value captured by the expression /<int:topic_id>/ .
    """ Show a single topic and all its entries. """
    # topic and entries are queries, for check if this is ok, test it in Django shell
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added') # the '-' sorts the results in reverse order. 
    context = {'topic':topic , 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

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
        if form.is_valid(): # Checks that all required fields have been filled in and that the data                   
            form.save()     # entered matches the field type expected. ej: the length we specified in models.py .
            return redirect('learning_logs:topics') 
            # redirect is used to redirect the user back to the topics page after they submit their topic

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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

def edit_entry(request, entry_id):
    """ Edit an existing entry. """
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

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
            books = Book.objects.filter(name__icontains=name)
            context = {'name': name,'books': books}
            return render(request, 'learning_logs/book_finder.html', context)
    else:
        form = BookFinderForm()
    
    context = {'form': form}
    return render(request, 'learning_logs/book_finder.html', context)

def NewBook(request):
    """ add a new particular book """
    if request.method != 'POST':
        form = BookForm()
    else:
        form = BookForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect ('learning_logs:BookFinder')
    
    context = {'form':form}
    return render(request, 'learning_logs/new_book.html', context)


