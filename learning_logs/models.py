from django.db import models

# Create your models here.
class Topic(models.Model):
    """ A topic the user is learning about. """
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """ Return a string representation of the model. """
        return self.text
    
class Entry(models.Model):
    """ Something specific learned about a topic. """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True) # It allows to present entries in the order they were created
    
    class Meta:
        verbose_name_plural = "entries"
        
    def __str__(self):
        """ Return a string representation of the model. """
        return f"{self.text[0:50]}..."
    
class Book(models.Model):
    """ Book you have read"""
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    description = models.TextField()