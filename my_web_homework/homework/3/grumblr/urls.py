from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login
import grumblr.views

urlpatterns = [
    url(r'^login$', login, {'template_name':'grumblr/signin.html'}, name='login'),        
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register, name='register'),
    url(r'^post$', grumblr.views.post, name='post'),
    url(r'^message$', grumblr.views.messagePost, name='stream'),
    url(r'^(?P<userid>\w+(?<![_.]))$', grumblr.views.users),
]
