from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#`posts model`
class Posts(models.Model):
    title =models.CharField(max_length=100)
    content =models.TextField()
    author =models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#`comment model`
class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"comment by {self.author.username} on {self.post.title}"