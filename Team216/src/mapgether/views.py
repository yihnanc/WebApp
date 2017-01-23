from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from mapgether.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
#Helper function to guess a MIME type from a file name
from mimetypes import guess_type
from django.http import HttpResponse, Http404

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator

# Add calendar
import datetime
from icalendar import Calendar, Event
import pytz

# Using Geocoding API
import urllib.request as urllib2

# For or operation query
from django.db.models import Q

# Avoid injection
from django.utils.html import escape

import os
import json

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

# map center location config
CENTER_LAT = float(40.443466)
CENTER_LNG = float(-79.943457)

from mapgether.models import *
from mapgether.forms import *

# adding html_comment in Comment Model before json.dumps
# json.dumps will remove @property html_comment
def add_html_comment(context, comments):
    # add .html_comment into the fields
    for i in range(len(context['comments'])):
        context['comments'][i]['fields']['html_comment'] = comments[i].html_comment
        #print("\n\nhtml_comment {0}\n\n".format(context['comments'][i]['fields']['html_comment']))

    #print("\nafter adding\n{0} {1}".format(context['comments'], len(context['comments'])))

@login_required
def user_tag(request):

    MAX_TAG = 5


    context = {}
    profile = Profile.objects.get(user=request.user)
    context["profile"] = profile
    context["username"] = request.user.username
    context['tags'] = Tag.objects.all()

    if request.method == 'GET':
        return render(request, 'mapgether/profile.html', context)

    tag_form = UserTagForm(request.POST)

    if not tag_form.is_valid():
        context['form'] = tag_form
        print("Add tag error")
        return render(request, 'mapgether/profile.html', context)

    tagnames = tag_form.cleaned_data['tags'].split(',')
    if len(tagnames) > MAX_TAG:
        context['tagmessage'] = "You can only add 5 tags"
        return render(request, 'mapgether/profile.html', context)

    
    #for tag in profile.choosetag.all():
    #    print("Original {0}\n\n".format(tag.tagname))
    
    # Remove orignal tags record
    profile.choosetag.clear()
    tag_list = ""

    for tag in tagnames:
        if len(tag.strip()) == 0: #ignore empty name
            continue
        # add to profile
        t = Tag.objects.get(tagname=tag.strip())
        profile.choosetag.add(t)

        tag_list += "'"+ tag.strip() +"' "  
        

    profile.save()
    
    context['tagmessage'] = "Successfully add tags " + tag_list

    return render(request, 'mapgether/profile.html', context)

@login_required
def addcomment(request, id):

    context = {}
    # check if user has privilege to see/add comment to that event
    
    # First check if the user in the attenduser list
    event = Event.objects.filter(id=id, attenduser__in=[request.user]).first()
    if event == None:
        print("add comment: Not attenduser")
        # check if the user is the owner
        event = Event.objects.filter(id=id, owner=request.user).first()

    # if user is the owner
    if event == None:
        print("add comment Not owner and attend user")
        event = Event.objects.filter(id=id, privacy=False).first()

    # if the event is public privacy=False
    if event == None:
        print("add comment Not owner and attend user and not public")
        raise Http404

    if request.method == 'GET':
        comments = Comment.objects.filter(event=event.id)
        comments = comments.extra(order_by=['added_time'])

        # get event coments
        context['comments'] = serializers.serialize('python', comments)
        
        # adding html_comment to the field
        add_html_comment(context, comments)
        
        context['comments'] = json.dumps(context['comments'], cls=DjangoJSONEncoder)

        return HttpResponse(json.dumps(context))

    # For POST case

    form = CommentForm(request.POST)
    if not form.is_valid():
        print("comment is not valid")
        #print(form)
        return(request, 'mapgether/home.html')

    new_comment = Comment(text = escape(form.cleaned_data['text']),
                          event = event,
                          user = request.user
                          )
    new_comment.save()

    comments = Comment.objects.filter(event=event.id)
    comments = comments.extra(order_by=['added_time'])


    # get event coments
    context['comments'] = serializers.serialize('python', comments)

    # adding html_comment to the field
    add_html_comment(context, comments)

    context['comments'] = json.dumps(context['comments'], cls=DjangoJSONEncoder)

    return HttpResponse(json.dumps(context))


@login_required
def add_tags(request):

    # Test webpage url http://127.0.0.1:8000/mapgether/add-tags
    
    context = {}
    # Due to the tags and profile now in the same page,
    # add_tags needs to put user profile information, and in
    # editprofile add to put tags information
    # (better way is to use redirect if in the final design, tag and profile
    # will be in the same page)
    profile = Profile.objects.get(user=request.user)
    context["profile"] = profile
    context["username"] = request.user.username

    if request.method == 'GET':
        #context['username'] = request.user
        #return render(request, 'mapgether/profile.html', context)
        context['tags'] = Tag.objects.all()
        return render(request, 'mapgether/profile.html', context)
    
    tag_form = TagForm(request.POST)

    # Validates the form
    if not tag_form.is_valid():
        #print("\nCreate event fail {0}\n".format(tag_form.errors))
        context['tagerrors'] = tag_form
        context['tags'] = Tag.objects.all()
        return render(request, 'mapgether/profile.html', context)

    tagnames = tag_form.cleaned_data['tags'].split(',')

    for tag in tagnames:
        if len(tag.strip()) == 0: #ignore empty name
            continue
        else:
            # check if the tag is in database
            if Tag.objects.filter(tagname__exact = tag):
                #duplicate
                print("duplicate tag {0}".format(tag))
                continue
            else:
                print("add tag {0}".format(tag))
                t = Tag.objects.create(tagname=tag)
                t.save()
    
    # show tag
    context['tags'] = Tag.objects.all()

    # debug
    return render(request, 'mapgether/profile.html', context)



@login_required
def profile(request):
    context = {'username': request.user.username}
    
    profile = Profile.objects.get(user=request.user)
    
    context['profile'] = profile
    context['tags'] = Tag.objects.all()

    return render(request, 'mapgether/profile.html',context)

@login_required
def linkProfile(request, userid):
    context = {'username': userid}
    user = get_object_or_404(User, username=userid)
    profile = Profile.objects.get(user=user)
    context['profile'] = profile
    context['tags'] = Tag.objects.all()

    return render(request, 'mapgether/profile.html',context)

@login_required
def get_photo(request, id):
    profile_user = get_object_or_404(Profile, user_id=id)
    if not profile_user.image:
        raise Http404

    content_type = guess_type(profile_user.image.name)
    return HttpResponse(profile_user.image, content_type=content_type)

@login_required
@transaction.atomic
def editprofile(request):
    id_user = request.user.id

    profile_edit = get_object_or_404(Profile, user=request.user, user_id=id_user)

    # Due to the tags and profile now in the same page,
    # add_tags needs to put user profile information, and in
    # editprofile add to put tags information
    # (better way is to use redirect if in the final design, tag and profile
    # will be in the same page)
    context = {'profile': profile_edit}
    context['tags'] = Tag.objects.all()
    context['username'] = request.user

    if request.method == 'GET':
        return render(request, 'mapgether/edit_profile.html', context)

    # if POST
     
    user_profile = Profile.objects.get(user_id=id_user)
    
    form_profile = ProfileForm(request.POST, request.FILES, instance=user_profile)

    if not form_profile.is_valid():
        context = {'form':form_profile}
        context['profile'] = user_profile
        return render(request, 'mapgether/temp_edit_profile.html', context)


    form_profile.save()

    return redirect(reverse('profile'), username = request.user)

def form_validate(request, event_form):
    # Validates the form
    if not event_form.is_valid():
        return None, event_form

    # check the address is valid
    geo_result = geocoding(escape(event_form.cleaned_data["address"]))

    if(geo_result["latitude"] is None):
        errors = "The address can't be found in GoogleMap. Please correct it"
        return None, errors
        #return render(request, 'mapgether/event.html', context)

    latitude = geo_result["latitude"]
    longitude = geo_result["longitude"]

    # Unified Time format
    # There are two time format:
    # (1) 2016-11-20T12:59     (user input)
    # (2) 2016-11-23 15:00:00  (ics file)
    unified_timezone = "US/Eastern"
    fmt = '%Y-%m-%dT%H:%M'

    # The tzinfo need to set None. Otherwise, it will become
    # 2016-11-29 12:59:00-05:00 not 2016-11-29 12:59:00
    start_time = pytz.timezone(unified_timezone).localize(
        datetime.datetime.strptime(event_form.cleaned_data['start_time'], fmt)).replace(tzinfo=None)

    end_time = pytz.timezone(unified_timezone).localize(
        datetime.datetime.strptime(event_form.cleaned_data['end_time'], fmt)).replace(tzinfo=None)

    trans_data = {'start_time':start_time, 'end_time':end_time, 'latitude':latitude, 'longitude':longitude}

    return event_form, trans_data

def save_event(event_form, eventobject):

    # Update many-to-many relationship
    # Save tag information
    eventobject.attenduser.clear()
    eventobject.tags.clear()

    tagnames = event_form.cleaned_data['tags'].split(',')
    for tag in tagnames:
        if len(tag.strip()) == 0: # ignore empty name
            continue
        t = Tag.objects.get(tagname=tag.strip())
        eventobject.tags.add(t)

    # Save attend user information
    usernames = event_form.cleaned_data['attenduser'].split(',')
    for user in usernames:
        if len(user.strip()) == 0: # ignore empty name
            continue
        u = User.objects.get(username=user.strip())
        eventobject.attenduser.add(u)

    eventobject.save()

    #print("hello check {0} {1}\n\n".format(eventobject.modified, eventobject.created))


@login_required
@transaction.atomic
def create_event(request):

    context = {'username': request.user}
    context['create']="createEvent"

    if request.method == 'GET':
        
        # for edit event
        return render(request, 'mapgether/event.html', context)

    # save the event if passing form validation or address is valid

    new_event = Event(owner=request.user)
    event_form = EventForm(request.POST, instance=new_event, username=request.user)
    
    event_form, trans_data = form_validate(request, event_form)

    #validation fail
    if event_form == None:

        if type(trans_data) is str:
            context['errors'] = trans_data
            #print(trans_data)
        else:
            context['form'] = trans_data
        return render(request, 'mapgether/event.html', context)

    e = Event.objects.create(title=escape(event_form.cleaned_data['title']),
                             start_time=escape(trans_data['start_time']),
                             end_time=escape(trans_data['end_time']),
                             latitude=trans_data['latitude'],
                             longitude=trans_data['longitude'],
                             address=escape(event_form.cleaned_data['address']),
                             description=escape(event_form.cleaned_data['description']),
                             owner=request.user,
                             privacy=event_form.cleaned_data['privacy'])
    save_event(event_form, e)

    return redirect(reverse('home'), username = request.user)

@login_required
@transaction.atomic
def edit_event(request, id):
    username = request.user

    event_to_edit = get_object_or_404(Event, owner=request.user, id=id)
    # change the time format to HTML5 datetime-local
    event_to_edit.start_time = event_to_edit.start_time.replace(" ", "T")[:-3]
    event_to_edit.end_time = event_to_edit.end_time.replace(" ", "T")[:-3]
    context = {'event': event_to_edit, 'id':id}

    init = 0
    # get tags and attenduser
    for tag in event_to_edit.tags.all():
        if (init == 0):
            context['tags'] = tag.tagname + ","
            init += 1
        else:
            context['tags'] += tag.tagname + ","
    
    init = 0

    for attenduser in event_to_edit.attenduser.all():
        if (init == 0):
            context['attendusers'] = attenduser.username + ","
            init += 1
        else:
            context['attendusers'] += attenduser.username + ","


    if request.method == 'GET':
        return render(request, 'mapgether/event.html', context)

    # POST request, update the database
    # Check validation

    event_form = EditEventForm(request.POST, username=request.user)
    event_form, trans_data = form_validate(request, event_form)   

    #validation fail
    if event_form == None:
        if type(trans_data) is str:
            context['errors'] = trans_data
        else:
            context['form'] = trans_data
        return render(request, 'mapgether/event.html', context)

    event_to_edit.title=escape(event_form.cleaned_data['title'])
    event_to_edit.start_time=escape(trans_data['start_time'])
    event_to_edit.end_time=escape(trans_data['end_time'])
    event_to_edit.latitude=trans_data['latitude']
    event_to_edit.longitude=trans_data['longitude']
    event_to_edit.address=escape(event_form.cleaned_data['address'])
    event_to_edit.description=escape(event_form.cleaned_data['description'])
    event_to_edit.privacy=escape(event_form.cleaned_data['privacy'])

    save_event(event_form, event_to_edit)

    return redirect(reverse('home'), username = request.user)

def update_event_time(request):
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user)
        profile.eventTime = timezone.now()
        print(profile.eventTime)
        profile.save()
    return redirect(reverse('home'), username = request.user)
    #return HttpResponse(json.dumps(context))

def update_notification(request):
    context ={}
    if request.user.is_authenticated():
        profile = Profile.objects.get(user=request.user);
        time = profile.eventTime;
        context['events'] = serializers.serialize('python',Event.objects.filter(attenduser=request.user,modified__gt=time))
        context['events'] = json.dumps(context['events'], cls=DjangoJSONEncoder)
        #print(context['events'])
        return HttpResponse(json.dumps(context))
    else:
        return HttpResponse(json.dumps({}))

@login_required
@transaction.atomic
def addcalendar(request):
    username = request.user

    # Check for GET or POST request
    if request.method == 'GET':
        return redirect(reverse('home'), username = username)

    #print("\nStarting to pare ics file\n")

    # For web
    # 1. form validation of input file
    # 2. Parsing input
    # 3. Store in database (need to deal with replica event)
    # 4. in case of uploading a large file, put limit data size

    # request.FILES already open file, so no need to open file again
    input_fd = request.FILES['filename_calendar']
    
    context = {}
    fmt = '%Y-%m-%d %H:%M:%S'
    # timeojbect.strftime(fmt)

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['tags'] = Tag.objects.all()
    context["username"] = request.user.username

    # check if the filesize is too large
    input_fd.seek(0,2)
    calendar_size = input_fd.tell()
    MAX_ICS_SIZE = 1024 * 1024
    if calendar_size > MAX_ICS_SIZE:
        context["event_message"] = "The file size should be smalle than 1 MB bytes"
        #context["username"] = request.user.username
        return render(request, 'mapgether/profile.html', context)
    
    else:
        input_fd.seek(0,0)

    # This is one to one mapping between recordField and databaseField
    recordField = ["DTSTART", "DTEND", "LOCATION", "SUMMARY", "DESCRIPTION"]
    databaseField = ["start_time", "end_time", "address", "title", "description"]


    parseResult = parse_ics(input_fd, recordField, fmt)

    # Check if errors
    if parseResult["errors"]:
        context["event_message"] = parseResult["errors"]
        return render(request, 'mapgether/profile.html', context)
    

    # Check each event
    # 1) valid
    # 2) not duplicate (one owener, can't have a duplicate event)
    add_event = 0
    for event in parseResult["events"]:

        if(Event.objects.filter(owner=username, title__exact=event["SUMMARY"])):
            # ignore this event, because of duplicate
            print("\n Duplicate event Summary {0}, Location{1}\n".format(event["SUMMARY"], event["LOCATION"]))
            continue
        else:
            # validate the event
            database_event = {}
            for index, field in enumerate(recordField):
                database_event[databaseField[index]] = event[field]

            # add geocoding information to the database
            print("geocoding address {0}".format(database_event["address"]))
            geo_result = geocoding(escape(database_event["address"]))

            # Ignore the geo_result if {"latitude": lat, "longitude": lng} is None
            if(geo_result["latitude"] is None):
                print("Ingore invalid address")
                continue
            else:
                database_event.update(geo_result)


            # form validate
            new_event = Event(owner=username)
            form = EventForm(database_event, instance=new_event, username=request.user)

            if not form.is_valid():
                # ignore this event, because of invalid input
                print(form.errors)
                print("Error in form validation")
                continue

            form.save()
            add_event += 1

    #print("\nEnd of paring ics file\n")
    if(add_event > 0):
        context['event_message'] = "Upload ics success. Total %s events are added." % (add_event)
    else:
        context['event_message'] = "No event is added. Either the title is duplicate or the format is incorrect."

    return render(request, 'mapgether/profile.html', context)
    #return redirect(reverse('profile'), context)

def geocoding(address):
    #ToDo need to remove this one when integrations
    GOOGLE_API_KEY = "AIzaSyDI0z-n-2hJ_dvCTYW4YvRK3h6CsmySikc"

    address_url = urllib2.quote(address)
    # address_url = address
    # format
    # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address_url, GOOGLE_API_KEY)

    request = urllib2.Request(geocode_url)
    response = urllib2.urlopen(request)
    jsonResponse = json.loads(response.read().decode(response.headers.get_content_charset()))

    # check status
    if (jsonResponse["status"] == 'OK'):
        # Get 'location' lng and lat
        # When returning several result because of ambiguity of address. take the first one
        geo = jsonResponse["results"][0]
        lat = geo["geometry"]["location"]["lat"]
        lng = geo["geometry"]["location"]["lng"]

        # To the precision .7f
        #lat = float("{:.7f}".format(lat))
        #lng = float("{:.7f}".format(lng))
        lat = round(lat, 7)
        lng = round(lng, 7)
        #print("\n\nlat {0}, lng {1}\n\n".format(lat, lng))

    else:
        # Error happen, print them in console
        lat = None
        lng = None
        #print("Using Google Geocoding API Error, Error status is {0}".format(jsonResponse["status"]))

    return ({"latitude": lat, "longitude": lng})


def parse_ics(input_fd, recordField, fmt):

    # if the time of parsed event is smaller than current time,
    # discarding the event

    # also need to fix time zone
    unified_timezone = "US/Eastern"
    current_time = pytz.timezone(unified_timezone).localize(datetime.datetime.now())

    # Store error message
    errors = ""
    events = []

    # traverse the calendar

    try:
        gcal = Calendar.from_ical(input_fd.read())
    except ValueError:
        errors = "The file type is incorrect. Please use .ics files and correct format"
        return {"errors": errors, "events": events}
    except KeyError:
        errors = "The file format is incorrect. Please use .ics files and correct format"
        return {"errors": errors, "events": events}
    except:
        errors = "The file is incorrect. Please use .ics files and correct format"
        return {"errors": errors, "events": events}

    # vcalendar attribute
    if not("x-wr-timezone" in gcal):
        # use default time zone
        cal_timezone = "US/Eastern"
    else:
        cal_timezone = gcal["x-wr-timezone"]

    if not (cal_timezone in pytz.common_timezones):
        errors = "The time zone in .ics file is undefined: %s" % (cal_timezone)

    else:
        for event in gcal.walk('vevent'):

            store_event = {}

            for field in recordField:

                if field == "DTSTART":
                    # check the time after current_time
                    # There is a possibility that it only contains date and no time
                    # DTSTART;VALUE=DATE:20160913
                    # Default value for DTSTART is 8:00AM
                    default_time = datetime.datetime(2000, 1, 1, 8, 0, 0)  # only care about (8, 0, 0)
                    event_time = _change_timezone(event[field].dt, pytz.timezone(unified_timezone),
                                                  default_time)

                    if (not event_time) or (event_time < current_time):
                        # ignore this event
                        break
                    else:
                        # store the time
                        store_event[field] = str(event_time.strftime(fmt))

                elif field == "DTEND":
                    # Default value for DTSTART is 5:00PM
                    default_time = datetime.datetime(2000, 1, 1, 17, 0, 0)  # only care about (8, 0, 0)
                    event_time = _change_timezone(event[field].dt, pytz.timezone(unified_timezone),
                                                  default_time)

                    if (not event_time) or (event_time < current_time):
                        # ignore this event
                        break
                    else:
                        # store the time
                        store_event[field] = event_time.strftime(fmt)

                elif field == "LOCATION":
                    # check empty string of location
                    if len(event[field]) == 0:
                        # ignore this event
                        # debug
                        break

                    else:
                        # store location
                        store_event[field] = event[field]

                elif field == "SUMMARY":
                    # check empyt string of summary
                    if len(event[field]) == 0:
                        # ignore this event
                        break

                    else:
                        # store summary
                        store_event[field] = event[field]
                else:
                # Store other fields
                    #print("{0}\n\n".format(event[field]))
                    store_event[field] = str(event[field])

            # store data that have "DTSTART", "DTEND", "LOCATION", "SUMMARY" field
            if (("DTSTART" in store_event) and \
                ("DTEND" in store_event) and \
                ("SUMMARY" in store_event) and \
                ("LOCATION" in store_event)):

                # if descrition is empty, assign the value of summary to it
                if (not "DESCRIPTION" in store_event) or (len(store_event["DESCRIPTION"]) == 0):
                    store_event["DESCRIPTION"] = store_event["SUMMARY"]

                events.append(store_event)

    if len(events) == 0:
        errors = "No event is added. Either the title is duplicate or the format is incorrect."

    return {"errors": errors, "events": events}

def _change_timezone(timeobj, timezone, default_time):
    """
    change datetime.datetime to timezone. If has datatime.date, combine it with default_time to
    become datetime.datetime object

    :param timeobj:
    :param timezone:
    :param default_time:
    :return:
    """

    if type(timeobj) is datetime.datetime and timeobj.tzinfo is not None:
        return timeobj.astimezone(timezone)

    elif type(timeobj) is datetime.datetime:
        return timezone.localize(timeobj)

    elif type(timeobj) is datetime.date:
        con = timezone.localize(datetime.datetime.combine(timeobj, default_time.time()))
        return con

    else:
        # unrecognized data type
        return None

def get_event_by_id(request, id):
    e = get_object_or_404(Event, id=id)
    data = serializers.serialize('python', e)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

def get_event_by_title(request, search_prefix = False):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404

    q = request.GET.get('term', '')
    events = Event.objects.filter(title__icontains=q)

    results = []
    for event in events:
        event_json = {}
        event_json['id'] = event.id
        event_json['label'] = event.title
        if search_prefix:
            event_json['value'] = '~' + event.title
        else:
            event_json['value'] = event.title
        results.append(event_json)

    return HttpResponse(json.dumps(results))

def get_attenduser(request):
    form = GetAttendTagForm(request.GET)
    if not form.is_valid():
        print(form.errors)
        raise Http404

    context = {}
    event = Event.objects.get(id=form.cleaned_data['eventid'])
    context['attendusers'] = serializers.serialize('python',
            event.attenduser.all(),
            fields=('username', 'first_name', 'last_name', 'email'))
    context['attendusers'] = json.dumps(context['attendusers'], cls=DjangoJSONEncoder)
    print(context)
    return HttpResponse(json.dumps(context))

def get_tagnames(request):
    form = GetAttendTagForm(request.GET)
    if not form.is_valid():
        print(form.errors)
        raise Http404

    context = {}
    context['tags'] = []
    event = Event.objects.get(id=form.cleaned_data['eventid'])
    for tag in event.tags.all():
        context['tags'].append(tag.tagname)
    print(context)
    return HttpResponse(json.dumps(context))

def get_event_by_location(request, lat, lng):
    context = {}
    context['user'] = ""
    context['events'] = serializers.serialize('python',
        Event.objects.filter(latitude=float(lat), longitude=float(lng)))
    context['events'] = json.dumps(context['events'], cls=DjangoJSONEncoder)

    if request.user.is_authenticated():
        context['user'] = serializers.serialize('python',User.objects.filter(username=request.user))
        context['user'] = json.dumps(context['user'], cls=DjangoJSONEncoder)
    return HttpResponse(json.dumps(context))

def get_tags(request, search_prefix = False):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404

    q = request.GET.get('term', '')
    tags = Tag.objects.filter(tagname__icontains=q)

    results = []
    for tag in tags:
        tag_json = {}
        tag_json['id'] = tag.tagname
        tag_json['label'] = tag.tagname
        if search_prefix:
            tag_json['value'] = '#' + tag.tagname
        else:
            tag_json['value'] = tag.tagname
        results.append(tag_json)

    return HttpResponse(json.dumps(results))

def get_usernames(request, search_prefix = False):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404

    q = request.GET.get('term', '')
    split_name = q.split(' ')
    firstname = split_name[0]

    if len(split_name) <= 1:
        users = User.objects.filter(first_name__icontains=firstname)
    else:
        lastname = split_name[1]
        users = User.objects.filter(first_name__icontains=firstname,
                last_name__icontains=lastname)

    results = []
    for user in users:
        user_json = {}
        user_json['id'] = user.id
        user_json['label'] = user.first_name + ' ' + user.last_name + ' <' + user.email + '>'
        if search_prefix:
            user_json['value'] = '@' + user.username
        else:
            user_json['value'] = user.username
        results.append(user_json)

    return HttpResponse(json.dumps(results))

def search(request):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404
    q = request.GET.get('term', '')
    request.GET = request.GET.copy()
    request.GET['term'] = q[1:] # remove prefix as the search term

    if q[0] == '#': # search tag
        return get_tags(request, True)
    elif q[0] == '@': # search people
        return get_usernames(request, True)
    elif q[0] == '~': # search event
        return get_event_by_title(request, True)
    else: # not a vaild prefix
        return HttpResponse(json.dumps({}))

@login_required
def join(request):
    form = JoinDropForm(request.POST)
    context = {}
    context['form'] = form

    if not form.is_valid():
        print(form.errors)
        raise Http404

    user = User.objects.get(id=form.cleaned_data['userid'])
    event = Event.objects.get(id=form.cleaned_data['eventid'])
    event.attenduser.add(user)

    return HttpResponse(request, context)

@login_required
def drop(request):
    form = JoinDropForm(request.POST)
    context = {}
    context['form'] = form

    if not form.is_valid():
        print(form.errors)
        raise Http404

    user = User.objects.get(id=form.cleaned_data['userid'])
    event = Event.objects.get(id=form.cleaned_data['eventid'])
    event.attenduser.remove(user)

    return HttpResponse(request, context)

"""
" new_map: Send JSON response of event locations to client for showing maps.
"
" When receiving new_map requests from client side's javascript, query the
" database for all events with location information and send the result back.
"""
def new_map(request, event_id = -1, tag_id = -1):
    context = {}
    context['user'] = ""
    context['center-lat'] = CENTER_LAT
    context['center-lng'] = CENTER_LNG
    events = Event.objects.filter(latitude__isnull=False)
    if event_id > -1:
        events = events.filter(id=event_id)
    elif tag_id > -1:
        events = events.filter(tags__id=tag_id)
    context['events'] = serializers.serialize('python', events)

    context['events'] = json.dumps(context['events'], cls=DjangoJSONEncoder)
    if request.user.is_authenticated():
        context['user'] = serializers.serialize('python',User.objects.filter(username=request.user))
        context['user'] = json.dumps(context['user'], cls=DjangoJSONEncoder)
    #print(context);
    return HttpResponse(json.dumps(context))

def new_specific_event_map(request, title):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404
    e = get_object_or_404(Event, title=title)
    return new_map(request, e.id, -1)

def new_tag_event_map(request, name):
    if not request.is_ajax: # disallow non-ajax requests
        raise Http404
    t = get_object_or_404(Tag, tagname=name)
    return new_map(request, -1, t.id)

def home(request):
    context = {}
    context['key'] = GOOGLE_API_KEY
    try:
        users = User.objects.get(username=request.user)
    except ObjectDoesNotExist:
        return render(request, 'mapgether/home.html', context)
    context['username'] = request.user

    profile = Profile.objects.get(user=request.user)
    context['user_tags'] = profile.choosetag.all()

    return render(request, 'mapgether/home.html', context)

@transaction.atomic
def login_form(request):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'mapgether/login_form.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    #Validate the form.
    if not form.is_valid():
        return render(request, 'mapgether/login_form.html', context)

    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username,password=password)
    print(username)

    login(request, user)
    return redirect('/home', username = username)
    #return render(request, 'mapgether/profile.html',{'username': request.user.username})
    #return render(request, 'mapgether/home.html',context)

@transaction.atomic
def register_form(request):
    context = {}

    #Display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'mapgether/register_form.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    #Validate the form.
    if not form.is_valid():
        return render(request, 'mapgether/register_form.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
    new_user.save()

    context['key'] = GOOGLE_API_KEY
    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']
    new_user = authenticate(username=username,password=password)
    login(request, new_user)

    # Create a empty profile
    # wait user for later update
    new_profile = Profile(user=new_user)
    new_profile.save()

    return redirect('/home', username = username)
