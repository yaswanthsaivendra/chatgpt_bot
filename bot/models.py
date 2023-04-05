from django.db import models

# Create your models here.


class Conversation(models.Model):
    sender = models.CharField(max_length=200)
    message = models.TextField()
    response = models.TextField()


    def __str__(self) -> str:
        return f"{self.sender}"