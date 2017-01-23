from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tag(models.Model):
    tagname  = models.CharField(max_length=50, blank=False)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length = 150, blank=False)
    start_time = models.CharField(max_length = 150,blank = False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    end_time = models.CharField(max_length = 150, blank = False)
    address = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=1000, blank=False)

    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, blank=True)

    attenduser = models.ManyToManyField(User, blank=True, related_name="attending")
    # True means private, False means public
    privacy = models.BooleanField(blank=False, default=True)

    # timestamp
    modified = models.DateTimeField()
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    occupation = models.CharField(max_length=256, blank=True)
    school = models.CharField(max_length=256, blank=True)
    age = models.IntegerField(default=20, blank=True)
    bio = models.CharField(max_length=420, default="", blank=True)
    image = models.ImageField(upload_to = 'user-picture', default='user-picture/default.png',blank="true")
    # timestamp
    eventTime = models.DateTimeField(auto_now=True)
    choosetag = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.bio
    def __str__(self):
        return self.bio

class Comment(models.Model):
    text = models.CharField(max_length=100)
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    added_time = models.DateTimeField(auto_now_add=True)

    @property
    def html_comment(self):
        # start
        total_html = "<div class='row'>"

        # image
        total_html += "<div class='col-xs-6 col-sm-2'>"
        total_html += "<img src='/mapgether/photo/%d' width='40px'>" % (self.user.id)
        total_html += "</div>"

        # name
        total_html += "<div class='col-xs-9 col-sm-12'>" 
        #total_html += "<p class='post-comment'><a class='comment-user' href='profile-view/%d' id='user_%d'>%s</a> %s </p>" % (self.user.id, self.user.id, self.user.username, self.added_time)
        total_html += "<p class='post-comment'><a class='comment-user' id='user_%d'>%s</a> %s </p>" % (self.user.id, self.user.username, self.added_time.strftime('%Y-%m-%d %H:%M:%S'))

        # comment content
        total_html += "<div class='post-content'>"
        total_html += "<p id='comment_%d'>%s</p>" % (self.id, self.text)

        # end first div: class='col-xs-9 col-sm-6'
        #     second div: class='post-content'
        #     third div: class='row'
        total_html += "</div></div></div>" 

        return total_html

    def __unicode__(self):
        return self.text
