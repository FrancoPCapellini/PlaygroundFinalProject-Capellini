""" Defines URL patterns for learning_logs. """
from django.urls import path
from . import views # el . quiere decir que importe desde el mismo directorio que esta urls.py

app_name = "learning_logs" # Namespace
urlpatterns = [ # is a list of individual pages that can be requested from the learning_logs app.
    # Home page
    path('',views.index, name = "index"),
    # Page that shows all topics.
    path('topics/', views.topics, name = 'topics'),
    # Detail page for a single topic. 
    path('topics/<int:topic_id>/', views.topic, name = 'topic'), # /<int:topic_id>/ captures a numerical value and assigns it to the variable topic_id.
    # Page for adding a new topic
    path('new_topic/', views.new_topic, name = 'new_topic'),
    # Page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'), # When a URL matching this pattern is requested, Django sends the request and the topic’s ID to the new_entry() view function.
    # Page for editinig an entry.
    path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry'),
    # Page for find books.
    path('find_book/', views.BookFinder, name = 'BookFinder'), 
    # Page for adding the book you read.
    path('new_book/', views.NewBook, name = 'NewBook'),
]

""" path() take 3 arguments
    first: route the request URL to a view.
    second: specific function to call in views.py.
    third: provides the name "index" for this URL.
"""