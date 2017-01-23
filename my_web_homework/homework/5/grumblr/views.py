from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.urlresolvers import reverse
from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required

#Nedded to manually create HttpResponses or raise an Http404 exception

#Helper function to guess a MIME type from a file name
from mimetypes import guess_type

#Used to send mail from within Django
from django.core.mail import send_mail

from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
from django.utils import timezone

from grumblr.models import *
from grumblr.forms import *

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
    profile_to_edit = get_object_or_404(Profile, owner=users)    
    form = ProfileForm(instance=profile_to_edit)          
    context['users'] = users
    #posts = Post.objects.filter(users=users).order_by('-created_date')
    #context['posts'] = posts
    context['form'] = form
    if users != request.user:
        return render(request, 'grumblr/users.html',context)
    else:    
        return render(request, 'grumblr/edit_prof.html', context)    

@login_required
@transaction.atomic()
def add_profile(request):
    try:
        #prevent user who has already created profile to add another profile
        prof = Profile.objects.get(owner=request.user)
        return redirect(reverse('stream'))    
    except ObjectDoesNotExist:
        if request.method == "GET":
            context = {'form':ProfileForm()}
            context['users'] = request.user
            return render(request, 'grumblr/add_prof.html', context)
        new_profile = Profile(owner=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=new_profile)
        if not form.is_valid():
            context = {'form':form}
            return render(request, 'grumblr/add_prof.html', context)
        form.save()
        context ={'username':request.user.username}
        return redirect(reverse('stream'))    

@login_required
def followerStream(request):
    context = {}
    #list_post=[]
    context['users'] = request.user
    #try:
    #    follower = Follow.objects.get(owner=request.user)
    #except ObjectDoesNotExist:
    #    posts = Post.objects.all().order_by('-created_date')
    #    context['posts'] = posts
    #    return render(request, 'grumblr/messagePost.html',context)
    #follower = Follow.objects.get(owner=request.user)
    #setFollowers = list(follower.follow.all())
    #for index in setFollowers:
    #    if list_post:
    #        current = Post.objects.filter(users=index)
    #        list_post = sorted(chain(list_post, current), key=attrgetter('created_date'),reverse=True)
    #    else:    
    #        list_post = Post.objects.filter(users=index).order_by('-created_date')
    #context['posts'] = list_post
    return render(request, 'grumblr/followerStream.html',context)        


@login_required
@transaction.atomic()
def edit_profile(request,userid):
    profile_to_edit = get_object_or_404(Profile, owner=request.user)    
    context = {}
    try:
        users = User.objects.get(username=userid)
    except ObjectDoesNotExist:
        context = {}
        if request.user != '':
            context['username'] = request.user
        return render(request, 'grumblr/home.html', context)
    if request.method == "GET":
        form = ProfileForm(instance=profile_to_edit)          
        posts = Post.objects.filter(users=request.user).order_by('-created_date')
        context = {'form':form, 'users':request.user, 'posts':posts}
        return  render(request, 'grumblr/edit_prof.html', context)  
    form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)
    if not form.is_valid():
        context = {'form':form, 'users':request.user} 
        return render(request, 'grumblr/edit_prof.html', context)
    form.save()     
    posts = Post.objects.filter(users=request.user).order_by('-created_date')
    context = {'form':form, 'users':request.user, 'posts':posts} 
    return render(request, 'grumblr/edit_prof.html', context)    

@login_required
@transaction.atomic()
def follow_user(request,userid):
    context = {}
    user = User.objects.get(username=userid)
    try:
        trace = Follow.objects.get(owner=request.user)
    except ObjectDoesNotExist:
        trace = Follow(owner=request.user)
        trace.save()
    trace.follow.add(user)    
    profile_to_return = get_object_or_404(Profile, owner=user)    
    form = ProfileForm(instance=profile_to_return)          
    context['users'] = user
    posts = Post.objects.filter(users=user).order_by('-created_date')
    context['posts'] = posts
    context['form'] = form
    return render(request, 'grumblr/users.html',context)

@login_required
@transaction.atomic()
def unfollow_user(request,userid):
    context = {}
    user = User.objects.get(username=userid)
    profile_to_return = get_object_or_404(Profile, owner=user)    
    form = ProfileForm(instance=profile_to_return)          
    context['users'] = user
    posts = Post.objects.filter(users=user).order_by('-created_date')
    context['posts'] = posts
    context['form'] = form
    try:
        trace = Follow.objects.get(owner=request.user)
    except ObjectDoesNotExist:
        return render(request, 'grumblr/users.html',context)
            
    trace.follow.remove(user)    
    return render(request, 'grumblr/users.html',context)

@login_required
def get_photo(request, userid):
    try:
        users = User.objects.get(username=userid)
    except ObjectDoesNotExist:
        context = {}
        if request.user != '':
            context['username'] = request.user
        return render(request, 'grumblr/home.html', context)
    entry = get_object_or_404(Profile, owner=users)
    if not entry.picture:
        raise Http404
    content_type = guess_type(entry.picture.name)
    return HttpResponse(entry.picture, content_type=content_type)

@login_required    
def messagePost(request):
    context = {}
    context['username'] = request.user
    #posts = Post.objects.all().order_by('-created_date')
    #context['posts'] = posts
    return render(request, 'grumblr/messagePost.html',context)

@login_required    
@transaction.atomic()
def addPost(request):
    form = PostForm(request.POST)
    if not form.is_valid():
        print("Post Input error")
        raise Http404
    now = datetime.now()
    now = now.strftime('%Y-%m-%d,%H:%M')
    new_post = Post(post=form.cleaned_data['post'],users=request.user,time=now)
    new_post.save()
    return HttpResponse("")

@login_required    
@transaction.atomic()
def addComment(request):
    form = CommentForm(request.POST)
    if not form.is_valid():
        print("Comment Input error")
        return HttpResponse("")
    try:
        post = Post.objects.get(id=request.POST['id'])
    except ObjectDoesNotExist:
        print("No corresponding postid")
        raise Http404
    now = datetime.now()
    now = now.strftime('%Y-%m-%d,%H:%M')
    new_comment = Comment(comment=form.cleaned_data['comment'],users=request.user,time=now, postid=post)
    new_comment.save()
    return HttpResponse("")

# Returns all recent changes to the database, as JSON                       
def get_streams(request, time="1970-01-01T00:00+00:00"):
#use aggregate in models.py to get the newest max-time
    max_time = Post.get_max_time()
    #use the  max time since last updated as the args, and filter it in the     models.py
    posts = Post.get_streams(time)
    context = {"max_time":max_time, "posts":posts} 
    return render(request, 'grumblr/posts.json', context, content_type='application/json')

def get_userStreams(request, userid, time="1970-01-01T00:00+00:00"):
#use aggregate in models.py to get the newest max-time
    try:
        users = User.objects.get(username=userid)
    except ObjectDoesNotExist:
        raise Http404
    max_time = Post.get_max_time()
    #use the  max time since last updated as the args, and filter it in the     models.py
    posts = Post.get_userStreams(users,time)
    context = {"max_time":max_time, "posts":posts} 
    return render(request, 'grumblr/posts.json', context, content_type='application/json')

def get_followerStreams(request, userid, time="1970-01-01T00:00+00:00"):
#use aggregate in models.py to get the newest max-time
    try:
        users = User.objects.get(username=userid)
    except ObjectDoesNotExist:
        raise Http404
    max_time = Post.get_max_time()
    #use the  max time since last updated as the args, and filter it in the     models.py
    posts = Post.get_followerStreams(users,time)
    #print("TestTestTest")
    #print(posts)
    context = {"max_time":max_time, "posts":posts} 
    return render(request, 'grumblr/posts.json', context, content_type='application/json')

def get_comments(request, postid, time="1970-01-01T00:00+00:00"):
#use aggregate in models.py to get the newest max-time
    max_time = Comment.get_max_time()
    #use the  max time since last updated as the args, and filter it in the     models.py
    comments = Comment.get_comments(postid, time)
    context = {"max_time":max_time, "comments":comments} 
    return render(request, 'grumblr/comments.json', context, content_type='application/json')

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

@transaction.atomic
def resetpwd_form(request):
    context = {}
    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ResetPwdForm()
        return render(request, 'grumblr/resetpwd_form.html', context)

    form = ResetPwdForm(request.POST) 
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/resetpwd_form.html', context)
        
    username = form.cleaned_data['username']
    user = User.objects.get(username__exact=username)
    token = default_token_generator.make_token(user)
    email_body = """
    You have sent a reqeust about password reset
    verify your email address and complete the passowrd reset for your account:
    http://%s%s
    """ % (request.get_host(),reverse('reset', args=(user.username, token)))

    send_mail(subject="Verify your email address for Grumblr password change",
              message=email_body,
              from_email="yihnanc@andrew.cmu.edu",
              recipient_list=[user.email]
            )

    context['email'] = user.email
    return render(request, 'grumblr/needs-resetpassword.html',context)

@login_required    
@transaction.atomic
def changepwd_form(request):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = ChangePwdForm()
        return render(request, 'grumblr/changepwd_form.html', context)

    form = ChangePwdForm(request.POST) 
    context['form'] = form

    #Validate the form.
    if not form.is_valid():
        return render(request, 'grumblr/changepwd_form.html', context)
        
    user = User.objects.get(username__exact=request.user.username)
    user.set_password(form.cleaned_data['new_passwd1'])
    user.save()        
    return redirect(reverse('logout'))    

@transaction.atomic
def real_reset(request, userid):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RealResetPwdForm()
        return render(request, 'grumblr/reset_confirm.html', context)

    form = RealResetPwdForm(request.POST) 
    context['form'] = form

    #Validate the form.
    if not form.is_valid():
        return render(request, 'grumblr/reset_confirm.html', context)
        
    user = User.objects.get(username__exact=userid)
    user.set_password(form.cleaned_data['new_passwd1'])
    user.save()        
    return redirect(reverse('logout'))    

@transaction.atomic
def confirm_reset(request, userid, token):
    #Display the registration form if this is a GET request
    context = {}
    context['username'] = userid
    context['form'] = RealResetPwdForm()
    return render(request, 'grumblr/reset_confirm.html', context)

@transaction.atomic
def confirm_register(request, userid, token):
    user = User.objects.get(username__exact = userid)
    user.is_active = True
    user.save()
    login(request, user)
    return redirect(reverse('add'))    

@transaction.atomic
def login_form(request):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'grumblr/login_form.html', context)

    form = LoginForm(request.POST) 
    context['form'] = form
    
    #Validate the form.
    if not form.is_valid():
        return render(request, 'grumblr/login_form.html', context)

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/grumblr/message', username = username)
        else:
            return render(request, 'grumblr/login_form.html', context)
    else:
        return render(request, 'grumblr/login_form.html', context)
        

@transaction.atomic
def register_form(request):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/register_form.html', context)

    form = RegistrationForm(request.POST) 
    context['form'] = form
    
    #Validate the form.
    if not form.is_valid():
        return render(request, 'grumblr/register_form.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password1'], \
                                        email=form.cleaned_data['email'],	\
                                        is_active=False
                                        )
    new_user.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to the Grumblr, Please click the ink below to
    verify your email address and complete the registration of your account:
    http://%s%s
    """ % (request.get_host(),reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address for Grumblr registration",
              message=email_body,
              from_email="yihnanc@andrew.cmu.edu",
              recipient_list=[new_user.email]
            )

    # Logs in the new user and redirects to his/her todo list
    #new_user = authenticate(username=form.cleaned_data['username'], \
   #                        password=form.cleaned_data['password1'])
    #login(request, new_user)
    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/needs-confirmation.html',context)

