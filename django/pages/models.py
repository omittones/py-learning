from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Post named '{self.name}'"

    # def __init__(self, *args, **kwargs):
    #     super.__init__(self, *args, **kwargs)