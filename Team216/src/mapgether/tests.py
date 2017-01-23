from django.test import TestCase, Client
from django.db import models
from django.contrib.auth.models import User
from mapgether.models import *
from mapgether.forms import *

class TagModelsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Sam', first_name="Sam", last_name="Yu", 
                                             password='1',
                                             email='fishrain23@gmail.com')
        self.profile = Profile.objects.create(user=self.user, occupation="cmu", school="cmu", age="20", bio="test")
        self.tag = Tag.objects.create(tagname="study")
        self.c = Client()

    def test_simple_add(self):
        self.assertTrue(Tag.objects.all().count() == 1)
        new_tag = Tag(tagname="ello")
        new_tag.save()
        self.assertTrue(Tag.objects.all().count() == 2)

    def test_wrongformat_add(self):
        context = {'tags':"12@321"}
        new_tag = TagForm(context)
        self.assertTrue(not new_tag.is_valid())

        context = {'tags':""}

class EventModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Sam', first_name="Sam", last_name="Yu", 
                                             password='1',
                                             email='fishrain23@gmail.com')
        self.profile = Profile.objects.create(user=self.user, occupation="cmu", school="cmu", age="20", bio="test")
        self.event = Event.objects.create(title="chalfont", start_time="2017-02-01T08:00", end_time="2017-02-03T08:00", address="4742 Centre Ave.", 
                                        description="Web demo", privacy="True", owner=self.user)
        self.c = Client()

    def test_simple_add(self):
        self.assertTrue(Event.objects.all().count() == 1)
        event = Event.objects.create(title="party", start_time="2017-02-01T08:00", end_time="2017-02-03T08:00", address="4742 Centre Ave.", 
                                        description="Web demo", privacy="True", owner=self.user)
        event.save()
        self.assertTrue(Event.objects.all().count() == 2)

    def test_duplicate_add(self):
        context = {'title':"chalfont", 'start_time':"2017-02-01T08:00", 'end_time':"2017-02-03T08:00", 'address':"4742 Centre Ave.", 
                                        'description':"Web demo", 'privacy':"True"}

        new_event = Event(owner=self.user)
        event_form = EventForm(context, instance=new_event, username=self.user)

        self.assertTrue( not event_form.is_valid())

class CommentModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Sam', first_name="Sam", last_name="Yu", 
                                             password='1',
                                             email='fishrain23@gmail.com')
        self.profile = Profile.objects.create(user=self.user, occupation="cmu", school="cmu", age="20", bio="test")
        
        self.event = Event.objects.create(title="chalfont", start_time="2017-02-01T08:00", end_time="2017-02-03T08:00", address="4742 Centre Ave.", 
                                        description="Web demo", privacy="True", owner=self.user)
        self.comment = Comment.objects.create(text="hi", event=self.event, user=self.user, added_time="2017-02-01T08:00")
        self.c = Client()


    def test_simple_add(self):
        self.assertTrue(Event.objects.all().count() == 1)
        comment = Comment.objects.create(text="hihi", event=self.event, user=self.user, added_time="2017-02-01T08:00")
        self.assertTrue(Comment.objects.all().count() == 2)



