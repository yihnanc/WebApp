from django import forms
#import floppyforms as forms

#from datetime import datetime

from django.forms import ModelForm, Textarea
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.utils.translation import ugettext_lazy as _
import datetime
import pytz

import re

from mapgether.models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'attenduser',)

    def clean_age(self):
        age_field = self.cleaned_data.get('age')
        if(age_field < 1 or age_field > 100):
            raise forms.ValidationError("Your age is no real. Please enter between 1 to 100")

        return age_field

    def clean_image(self):
        image_field = self.cleaned_data.get('image')
        if image_field._size > 1024*1024*2:
            raise forms.ValidationError("Please upload image smaller than 2MB")
        
        return image_field


class EventForm(forms.ModelForm):
    tags = forms.CharField(max_length=1000, required=False)
    attenduser = forms.CharField(max_length=200, required=False) # about 10 people
    class Meta:
        model = Event
        # Todo remove owner field and other manytomanyfield
        exclude = ('owner', 'tags', 'modified', 'created')

    def __init__(self, *args, **kwargs):
        # use self to store user
        self.form_username = kwargs.pop("username")
        super(EventForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        # check if the title is not present in database for this user
        username = User.objects.filter(id=self.form_username.id)
        title = self.cleaned_data.get('title')

        if Event.objects.filter(owner__exact=username, title__exact=title):
            raise forms.ValidationError("Event title is already taken. Change another title")
        return title

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        print(tags)
        if len(tags) == 0:
            return tags

        tag_dict = tags.split(',')

        for tag in tag_dict:
            if len(tag.strip()) == 0: # ignore empty name
                continue
            try:
                Tag.objects.get(tagname=tag.strip())
            except ObjectDoesNotExist:
                raise forms.ValidationError("Invalid tag")

        return tags

    def clean_attenduser(self):
        usernames = self.cleaned_data.get('attenduser')
        print(usernames)
        usernames_dict = usernames.split(',')

        for user in usernames_dict:
            if len(user.strip()) == 0: # ignore empty name
                continue
            try:
                User.objects.get(username=user.strip())
            except ObjectDoesNotExist:
                raise forms.ValidationError("Invalid attenduser")

        return usernames

    def clean(self):
        # check start and end time
        cleaned_data = super(EventForm, self).clean()

        # confirm that end time > start time, and start > current time
        unified_timezone = "US/Eastern"
        current_time = pytz.timezone(unified_timezone).localize(datetime.datetime.now())

        start_time_field = self.cleaned_data.get('start_time')
        end_time_field = self.cleaned_data.get('end_time')

        # input format 2016-11-26T01:01 from user (type is string)
        # input format from ics file (type is date time)
        fmt = '%Y-%m-%d %H:%M:%S'
        if "T" in start_time_field:
            fmt = '%Y-%m-%dT%H:%M'


        start_time_field = pytz.timezone(unified_timezone).localize(datetime.datetime.strptime(start_time_field, fmt))

        end_time_field = pytz.timezone(unified_timezone).localize(datetime.datetime.strptime(end_time_field, fmt))

        #print("in form validation {0}".format(cleaned_data))

        if(start_time_field < current_time):
            raise forms.ValidationError("The start time should be larger than current time")

        if(end_time_field < start_time_field):
            raise forms.ValidationError("The End time should be larger than start time")

        return cleaned_data

class UserTagForm(forms.Form):
    tags = forms.CharField(max_length=1000, required=False)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        print(tags)
        if len(tags) == 0:
            return tags

        tag_dict = tags.split(',')

        for tag in tag_dict:
            if len(tag.strip()) == 0: # ignore empty name
                continue
            try:
                Tag.objects.get(tagname=tag.strip())
            except ObjectDoesNotExist:
                raise forms.ValidationError("Invalid tag")

        return tags

class TagForm(forms.Form):
    tags = forms.CharField(max_length=1000, required=False)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        print(tags)
        if len(tags) == 0:
            return tags

        tag_dict = tags.split(',')

        for tag in tag_dict:
            if len(tag.strip()) == 0: # ignore empty name
                continue
            if bool(re.match("^[A-Za-z]+$", tag)) == False:
                raise forms.ValidationError("Invalid tag most be a-zA-Z")

        return tags

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'event',)

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,
    widget=forms.TextInput(attrs={'placeholder': 'Username',"class":"TextType"})
    )
    password = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput(attrs={"placeholder": "Password","class":"TextType"})
    )
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(LoginForm, self).clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username doesn't exist.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Password.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',"class":"TextType"}))

    first_name = forms.CharField(max_length = 20,
        widget=forms.TextInput(
            attrs={'placeholder': 'Firstname',"class":"TextType"}))

    last_name = forms.CharField(max_length = 20,
        widget=forms.TextInput(
            attrs={'placeholder': 'Lastname',"class":"TextType"}))


    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput(attrs={"placeholder": "Password","class":"TextType"})
    )
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput(attrs={"placeholder": "Confirm Password","class":"TextType"})
    )

    email = forms.EmailField(max_length = 30,
    widget=forms.TextInput(attrs={'placeholder': 'Email','class':'TextType'})
    )
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact = username):
            raise forms.ValidationError("Usernmae is already taken")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class EditEventForm(EventForm):
    #overwrite EventForm clean_title
    def clean_title(self):
        # check if the title is not present in database for this user
        title = self.cleaned_data.get('title')

        return title

    

class JoinDropForm(forms.Form):
    userid = forms.IntegerField(required=True)
    eventid = forms.IntegerField(required=True)

    def clean_userid(self):
        userid = self.cleaned_data.get('userid')
        try:
            user = User.objects.get(id=userid)
        except ObjectDoesNotExist:
            raise forms.ValidationError("User not found.")
        return userid

    def clean_eventid(self):
        eventid = self.cleaned_data.get('eventid')
        try:
            event = Event.objects.get(id=eventid)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Event not found.")
        return eventid
    # TODO: validate if the user is already in the attenduser

class GetAttendTagForm(forms.Form):
    eventid = forms.IntegerField(required=True)

    def clean_eventid(self):
        eventid = self.cleaned_data.get('eventid')
        try:
            event = Event.objects.get(id=eventid)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Event not found.")
        return eventid
