from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Mode):
    occupation = models.CharField(max_length=256, blank=True)
    School = models.CharField(max_length=256, blank=True)
    age = models.IntegerField(default=0, blank=True)
    picture = models.ImageField(upload_to="mapGather", blank=False)
    bio = models.CharField(max_length=420, default="", blank=False)
    def __unicode__(self):
        return self.bio
    def __str__(self):
        return self.bio

class Tag(models.Model):
    name = models.CharField(max_length=256, blank=False)
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=256, blank=False)
    time = models.DateTimeField(blank=False)
    address = models.CharField(max_length=256, blank=False)
    owner = models.ForeignKey(User)
    inviteduser = models.ManyToManyField(User, blank=True)
    tags = model.ManyToManyField(Tag, blank=False)
    description = models.TextField(blank=False)
    privacy = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.CharField(max_length=256, blank=False)
    time = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.text
