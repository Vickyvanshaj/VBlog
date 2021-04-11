from django.contrib import admin
from .models import Post,BlogComment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display=['id','title','author','content','timeStamp']
    class Media:
        js= ('tinyinject.js',)
@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display=['id','comment','user','post','parent','timestamp']