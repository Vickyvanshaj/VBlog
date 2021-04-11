from django.db import models

class Contact(models.Model):
    name=models.CharField(max_length=255,default='')
    phone=models.CharField(max_length=13)
    email=models.EmailField(max_length=100)
    content=models.TextField()
    timeStamp=models.DateField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from '+self.name
