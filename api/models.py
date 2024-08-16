from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.



class CustomUser(AbstractUser):
    phone=models.CharField(max_length=10)
    
class Users(CustomUser):
    name=models.CharField(max_length=100)
    email_id=models.EmailField(max_length=100)
    phone_number=models.CharField(max_length=10)
    
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    user= models.ForeignKey(Users, on_delete=models.CASCADE)  # Correct reference to CustomUser
    def __str__(self):
        return self.title
    
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Correct reference to CustomUser
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
    
    

    