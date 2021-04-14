from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=300)
    content=models.TextField(blank=True)
    author=models.CharField(max_length=100)
    timeStamp=models.DateTimeField(blank=True)
    slug=models.CharField(max_length=200)
    views=models.IntegerField(default=0)
    def __str__(self):
        return self.title+' by '+self.author


class BlogComment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13]+"..."+" by "+self.user.username

    