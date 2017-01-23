from django.conf.urls import include, url

import mapgether.views
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login


urlpatterns = [
    url(r'^addcalendar$', mapgether.views.addcalendar, name ='addcalendar_url'),
    url(r'^new-map$', mapgether.views.new_map),
    url(r'^new-specific-event-map/(?P<title>\w+)$', mapgether.views.new_specific_event_map),
    url(r'^new-tag-event-map/(?P<name>\w+)$', mapgether.views.new_tag_event_map, name='tag_event'),
    url(r'^profile$', mapgether.views.profile, name='profile'),
    url(r'^login$', mapgether.views.login_form, name='login'),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^register$', mapgether.views.register_form, name='register'),
    url(r'^get-event/(?P<id>\d+)$', mapgether.views.get_event_by_id),
    url(r'^get-event/(?P<lat>[-]?\d+.\d+),(?P<lng>[-]?\d+.\d+)$', mapgether.views.get_event_by_location),
    url(r'^get-usernames/', mapgether.views.get_usernames),
    url(r'^get-tagnames/', mapgether.views.get_tagnames),
    url(r'^get-tags/', mapgether.views.get_tags),
    url(r'^join$', mapgether.views.join),
    url(r'^drop$', mapgether.views.drop),
    url(r'^get-attenduser/', mapgether.views.get_attenduser),

    url(r'^create-event$', mapgether.views.create_event, name='create_event'),
    url(r'^edit-event/(?P<id>\d+)$', mapgether.views.edit_event, name='edit_event'),
    url(r'^edit-profile$', mapgether.views.editprofile, name='edit_profile'),
    url(r'^photo/(?P<id>\d+)$', mapgether.views.get_photo, name='user_photo'),
    url(r'^addcomment/(?P<id>\d+)$', mapgether.views.addcomment, name='add_comment'),
    url(r'^add-tags', mapgether.views.add_tags, name='add_tag'),
    url(r'^linkProfile/(?P<userid>\w+(?<![_.]))$', mapgether.views.linkProfile),
    url(r'^search/', mapgether.views.search),
    url(r'^user-tag$', mapgether.views.user_tag, name='user_tag'),

    url(r'^update-notification$', mapgether.views.update_notification, name='updates'),
    url(r'^updateTime', mapgether.views.update_event_time),
]
