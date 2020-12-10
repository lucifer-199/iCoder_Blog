from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog.models import Post

#HTML Pages
def home(request):
    return render(request,'home/home.html')

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method== 'POST':
        name= request.POST['name']        
        email= request.POST['email']        
        phone= request.POST['phone']        
        content= request.POST['content']  
        print(name, email, phone, content)   

        if len(name)<2 or len(email)<3 or len(email)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else :
            messages.success(request," Your message has been sent successfully ")
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()   
    return render(request,'home/contact.html')

def search(request):
    query =request.GET['query']
    if len(query)>78 :
        allPosts=Post.objects.none()
    else :
        allPoststitle= Post.objects.filter(title__icontains=query)
        allPostscontent= Post.objects.filter(content__icontains=query)
        allPosts=allPoststitle.union(allPostscontent)

    if allPosts.count()==0:
        messages.error(request,"No search results found. Please refine your query")
    params = {'allPosts': allPosts, 'query':query}
    return render(request,'home/search.html',params)
    
# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        #get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for eroneous inputs
        if len(username)>10:
            messages.error(request," Username must be under 10 character!")
            return redirect('home')
        if not username.isalnum():
            messages.error(request," Username should only contain alphanumeric characters!")
            return redirect('home')

        if(pass1 != pass2):
            messages.error(request,"Your password doesn't match!")
            return redirect('home')
        
        


        #create the user
        # myuser = User.objects.create_user(username, email, pass1)
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your iCoder Account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse('404- Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username = loginusername, password = loginpass)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return redirect('home')


    return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out!")
    return redirect('home')
