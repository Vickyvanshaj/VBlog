from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    allPosts=Post.objects.all().order_by('-views')
    context={'allPosts':allPosts}
    return render(request,'home/home.html',context)


def contact(request):
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Your message has been sent successfully.')
        

    return render(request,'home/contact.html')


def about(request):
    return render(request,'home/about.html')


def search(request):
    query=request.GET['query']
    if len(query)>100:
        allPosts=[]
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent)


    params={'allPosts':allPosts,'query':query}
    if len(allPosts)==0:
        messages.warning(request,"No Search results found!")
    else:
        messages.success(request,""+str(len(allPosts))+" results found!")
    return render(request,'home/search.html',params)



# Authentication APIs
def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        password=request.POST['password']
        password2=request.POST['password2']
        #checking for duplicates username and email
        emailCheck=User.objects.filter(email__icontains=email)
        usernameCheck=User.objects.filter(username__icontains=username)

        if len(username)>10:
            messages.error(request,'Username must be under 10 characters.')
            return redirect('home')
        if username.isalnum() == False:
            messages.error(request,'Username should only contain letter and numbers.')
            return redirect('home')
        if password != password2:
            messages.error(request,'Password not matched. Please enter same passwords.')
            return redirect('home')
        if len(emailCheck)>0:
            messages.error(request,'Email Already Registered.Try a new Email.')
            return redirect('home')
        elif len(usernameCheck)>0:
            messages.error(request,'Username Already Exists. Try a new Username.')
            return redirect('home')
        else:
            myuser=User.objects.create_user(username,email,password)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request,'Your Vblog account has been successfully created')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['pass']

        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials, please try again')
            return redirect('home')
    
    return HttpResponse('404 - Not Found')


def handleLogout(request):
        logout(request)
        messages.success(request,'Successfully logged out')
        return redirect('/')
        



