from django.urls import reverse
from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Post named '{self.name}'"

    def get_absolute_url(self):
        return reverse('post-details', kwargs = { "post_id" : self.pk })
