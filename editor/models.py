from django.db import models
from users.models import MainUser
from django.urls import reverse
import uuid

# Create your models here.

class PagesAi(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, verbose_name="User")
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=20, verbose_name="Title")
    time_create = models.DateField(auto_now_add=True, verbose_name="Create time")
    time_update = models.DateField(auto_now=True, verbose_name="Update_time")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home_detail', kwargs={'page_slug': self.slug})
    
class ChatMessages(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, verbose_name="User")
    chat = models.ForeignKey(PagesAi, on_delete=models.CASCADE, verbose_name="Chat", related_name='chat')
    text_user = models.TextField(verbose_name="Text_user")
    text_ai = models.TextField(verbose_name="Text_ai")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text_user[:30]}"