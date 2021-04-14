from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from blog.templatetags import extras
from .forms import PostForm


def blogHome(request):
    allPosts=Post.objects.all()
    context={'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)


def blogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    
    post.views=post.views+1
    post.save()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replDict={}
    for reply in replies:
        if reply.parent.id not in replDict.keys():
            replDict[reply.parent.id]=[reply]
        else:
            replDict[reply.parent.id].append(reply)
    print(replDict)

    context={'post':post,'comments':comments,'user':request.user,'count':len(comments),'replyDict':replDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        
        postId=request.POST.get('postId')
        parentId=request.POST.get('parentId')
        post=Post.objects.get(id=postId)
        if(parentId==""):
            
            comment=BlogComment.objects.create(user=user,comment=comment,post=post)
            # comment.save()
            messages.success(request,'Your comment has been added!')
        else:
            parent=BlogComment.objects.get(id=parentId)
            comment=BlogComment(user=user,comment=comment,post=post,parent=parent)
            comment.save()
            messages.success(request,'Your reply has been added!')


    return redirect(f'/blog/{post.slug}')


def handleLogin(request):
    if request.method == 'POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['pass']
        
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged in')
            return redirect('/blog')
        else:
            messages.error(request,'Invalid Credentials, please try again')
            return redirect('/blog')
    
    return HttpResponse('404 - Not Found')


def handleLogout(request):
        logout(request)
        messages.success(request,'Successfully logged out')
        return redirect('/blog')
 

def createBlog(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.timeStamp = timezone.now()
            post.save()
            
            return redirect(f'/blog/{post.slug}')
    else:
        form=PostForm()
    return render(request,'blog/createBlog.html',{'form':form})