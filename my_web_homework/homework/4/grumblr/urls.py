from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login
import grumblr.views

urlpatterns = [
    url(r'^login$', grumblr.views.login_form, name='login'),        
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', grumblr.views.register_form, name='register'),
    url(r'^changepwd$', grumblr.views.changepwd_form, name='chgpwd'),
    url(r'^resetpwd$', grumblr.views.resetpwd_form, name='checkmail'),
    url(r'^post$', grumblr.views.post, name='post'),
    url(r'^message$', grumblr.views.messagePost, name='stream'),
    url(r'^stream$', grumblr.views.followerStream, name='fstream'),
    url(r'^add_prof$', grumblr.views.add_profile, name='add'),
    url(r'^edit_prof/(?P<userid>\w+(?<![_.]))$', grumblr.views.edit_profile, name='edit'),
    url(r'^follow/(?P<userid>\w+(?<![_.]))$', grumblr.views.follow_user, name='follow'),
    url(r'^unfollow/(?P<userid>\w+(?<![_.]))$', grumblr.views.unfollow_user, name='unfollow'),
    url(r'^photo/(?P<userid>\w+(?<![_.]))$', grumblr.views.get_photo, name='photo'),
    url(r'^(?P<userid>\w+(?<![_.]))$', grumblr.views.users, name='users'),
    url(r'^confirm-registration/(?P<userid>\w+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', grumblr.views.confirm_register, name='confirm'),
    url(r'^reset-mail/(?P<userid>\w+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', grumblr.views.confirm_reset, name='reset'),
    url(r'^realreset/(?P<userid>\w+(?<![_.]))$', grumblr.views.real_reset, name='realreset'),
]
