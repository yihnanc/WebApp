from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from datetime import datetime
from django.utils import timezone

from grumblr.models import *

# Create your views here.

def home(request):
    context = {}
    try:
        users = User.objects.get(username=request.user)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/home.html',{})
    context['username'] = request.user
    return render(request, 'grumblr/home.html',context)

@login_required    
def users(request,userid):
    context = {}
    try:
        users = User.objects.get(username=userid)
    except ObjectDoesNotExist:
        context = {}
        if request.user != '':
            context['username'] = request.user
        return render(request, 'grumblr/home.html', context)
    context['users'] = users
    posts = Post.objects.filter(users=users).order_by('-created_date')
    context['posts'] = posts
    return render(request, 'grumblr/users.html',context)

@login_required    
def messagePost(request):
    context = {}
    context['username'] = request.user
    posts = Post.objects.all().order_by('-created_date')
    context['posts'] = posts
    return render(request, 'grumblr/messagePost.html',context)

@login_required    
def post(request):
    errors = []
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append("The post appears to be blank, Please write something")
    else:
        now = datetime.now()
        now = now.strftime('%Y-%m-%d,%H:%M')
        new_post = Post(post=request.POST['comment'],users=request.user,time=now)
        new_post.save()
    
    posts = Post.objects.all().order_by('-created_date')
    context = {'posts' : posts, 'errors' : errors, 'username' : request.user}
    return render(request, 'grumblr/messagePost.html', context)

def register(request):
    context = {}

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'grumblr/register.html', context)

    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if 'username' in request.POST and len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')
    
    if not 'firstname' in request.POST or not request.POST['firstname']:
        errors.append('First Name is required.')

    if not 'lastname' in request.POST or not request.POST['lastname']:
        errors.append('Last Name is required.')

    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email is required.')
    
    if "@" not in request.POST['email'] or request.POST['email'].startswith("@") or request.POST['email'].endswith("@"):
        errors.append("invalid email address(ex:xxx@yyyy.com)")

    if 'email' in request.POST and len(User.objects.filter(email = request.POST['email'])) > 0:
        errors.append('Email is already taken.')

    if errors:
        return render(request, 'grumblr/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password1'], \
                                        first_name=request.POST['firstname'], \
                                        last_name=request.POST['lastname'], \
                                        email=request.POST['email']
                                        )
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect('/grumblr/message', username = request.POST['username'])
    
