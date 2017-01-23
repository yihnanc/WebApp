    var currentMap;
var markers = [];
var debug_info;

function populate() { 
    getUpdates();
}

function showEventHTML(pk, fields, detail, lat, longt, isOwner=false, isAttending=false, userid, username) {
  var html = "";
  html += "<div class='row eventloc' id='" + pk + "' data-lat='" + lat + "' data-longt='" + longt + "'>";
  //html += '  <input class="input-control2" type="text" name="title" value="' + fields.title + '" readonly="readonly">';
  html += "<div class='col-md-10'>";
  html += "<h3 class='plan-title'>" + fields.title + "</h3>";
  html += "</div>";

  if(detail) {
    html += "<div class='col-md-2 eventdata' id='eventdata_" + pk + "' data-time='" + fields.start_time+ "' data-loc='" + fields.address + "' data-title='" + fields.title+ "' data-isowner='" + isOwner.toString() + "' data-isattending='" + isAttending.toString() + "' data-username='" + username + "' data-userid=" + userid + ">";
    html += '<button class="btn btn-success" data-index="' + pk + '" name="enlarge" data-lat="' +lat+ '" data-longt="' +longt+ '" data-descript="' + fields.description + '">';
    html += '  <i class="fa fa-search-plus fa-2x" aria-hidden="true"></i>';
    html += '</button>';
    html += "</div>";
  }

  html += '<ul class="plan-features">';
  html += '<li class="plan-feature">Time: <span name="startTime" class="plan-feature-name">' + fields.start_time + '</span></li>';
  html += '<li class="plan-feature">Location: <span name="addr" class="plan-feature-name">' + fields.address + '</span></li>';
  html += '</ul>';
  html += "</div>";
  html += "</div>";

  return html;
}
function eventNotification(number) {
  var html = "";
  if (number == 0) {
    html += '<a id="notify" class="nav-item btn btn-success" onClick="popout()">Notification:<span class="clean_show">' + number +'</span></a>';
  } else {
    html += '<a id="notify" class="nav-item btn btn-success" onClick="popout()">Notification:<span class="error_show">' + number +'</span></a>';
  }
  return html;
}
function showAttendUser(username) {
  var html = "";
  html += '<a class="btn btn-primary" href="/mapgether/linkProfile/'+username+'"><span class="content-friend">'+username+'</span></a>'
  return html;
}

function showTagName(tagname) {
  var html = "";
  html += '<a class="btn btn-primary" href="#"><span class="content-friend">'+tagname+'</span></a>'
  return html;
}

function showTitle(title, id) {
  var html = "";
  var realTitle = title.split(":")[1];
  html += '<li class="plan-feature">';
  html += '<button data-id="' + id + '" class="btn btn-success btn-lg jump" data-title="' + realTitle + '">'+ title + '</button>';
  html += '</li>';
  return html;
}
function popout(){
  var html = "";
  html += '<div id="dialog" title="Notification" class="input-control2">';
  html += '<ul class="plan-features">';
  html += '<div id="notifyTitle">';
  html += '</div>';
  html += '</ul>';
  html += '</div>';
  $("#eventNotification").append(html);

  $( "#dialog" ).dialog({   
        modal: true,   
        autoOpen: false,
        show: 'blind',
        hide: 'fold',
        draggable: false,
        resizable: false,
        position: { my: "right", at: "right-100px top+200px ", of: window  },
        height: 300,
        width: 350,
        dialogClass: 'zoomout no-close plan-button',
        buttons: {   
            "OK": function() {
                $(this).dialog("close");
                $('#eventNotification').empty(); 
                $.get("/mapgether/updateTime/")
                    .done(function(data) {
                        getUpdates();
                    });
                $("#dialog").empty();    
            },
        },   
        open: function() {
            var list = $('#eventNotification');
            str_events = [];
            str_events = list.data('events');
            var draw = $('#notifyTitle');
            $('.ui-dialog-buttonpane').find('button:contains("OK")').addClass("OKButton");
            for (var i = 0; i < str_events.length; i++) {
                if (typeof(str_events[i]) != "undefined") {
                    draw.append(showTitle(str_events[i],i));
                }
            }
            $('.jump').click(function(e) {
                var id = $(this).data("id");
                var title = $(this).data("title"); 
                specificEventMap(title);                
            });
        },
   });  
  $("#dialog").dialog("open");
}

function zoomout(e){
  var id = $(this).data("index");
  var lat = $(this).data("lat");
  var longt = $(this).data("longt");
  // if click on the icon, data is in parent().parent()
  var parent = $(e.target).parent();
  if (!!!parent.data("title")) {
    parent = $(e.target).parent().parent();
  }
  var title = parent.data("title");
  var time = parent.data("time");
  var addr = parent.data("loc");
  var isOwner = parent.data("isowner");
  var isAttending = parent.data("isattending");
  var userid = parent.data("userid");
  var useraccount = parent.data("username");

  var descript = $(this).data("descript");
  var position = {lat: lat, lng: longt}

  for (var i = 0; i < markers.length; i++) {
    if((markers[i].getPosition().lat() - lat) > 0.000001 || (markers[i].getPosition().lat() - lat) < -0.000001 ||
    (markers[i].getPosition().lng() - longt) > 0.000001 || (markers[i].getPosition().lng() - longt) < -0.000001)
    {
      markers[i].setMap(null);
    }
  }

  currentMap.setCenter(position);
  //remove previous dialog
  $("#favDialog").remove();
  $("#dialog-form").remove();

  var html = "";
  html += '<dialog id="favDialog">'
  html += '<div id="dialog-form" title="'+ title + '" class="input-control2">'

  // edit
  html += '  <button class="btn btn-success pull-right edit">';
  //html += '<a class="nav-item btn btn-success pull-right" href="{% url 'login' %}">';
  html += '    <i class="fa fa-pencil fa-2x" aria-hidden="true"></i>';
  //html += '</a>';
  html += '  </button>';

  // withdraw
  html += '  <button class="btn btn-success pull-right withdraw" id="withdraw_' + id + '">';
  html += '    <i class="fa fa-trash fa-2x" aria-hidden="true"></i>';
  html += '  </button>';

  // join
  html += '  <button class="btn btn-success pull-right join" id="join_' + id + '">Join';
  html += '  </button>';

  html += '<ul class="plan-features">';
  html += '<li class="plan-feature1">Time: <span name="startTime" class="plan-feature-name1">' + time + '</span></li>';
  html += '<li class="plan-feature1">Location: <span name="addr" class="plan-feature-name1">' + addr + '</span></li>';
  html += '</ul>';
  html += '<span class="plan-feature4"><textarea class="input-control3" name="discript" rows="20" readonly="readonly">' + descript + '</textarea></span>';
  //Show attenduser
  html += '<div id="showAttendUser"></div>'
  html += '<div id="showTagNames"></div>'

  // show comment
  html += '<div id="show-comment"></div>';

  // add comment
  html += '<div >';
  html += '<input name="text" id="comment_event_' + id + '">';
  html += '<button id="add-comment" class="btn btn-success">Comment</button>';
  html += '</div>'

  html += '</div>';
  html += '</dialog>';
  $("#events").append(html);

  if (isOwner) { // edit
    $('.edit').show();
    $('.join').hide();
    $('.withdraw').hide();
  } else if (isAttending) { // withdraw
    $('.edit').hide();
    $('.join').hide();
    $('.withdraw').show();
  } else { // join
    $('.edit').hide();
    $('.join').show();
    $('.withdraw').hide();
  }

  $("#dialog-form").dialog({
    autoOpen: false,
    show: 'blind',
    hide: 'explode',
    draggable: false,
    resizable: false,
    position: { my: "right", at: "right-400px top+600px ", of: window  },
    height: 650,
    width: 500,
    dialogClass: 'zoomout no-close plan-button',
    buttons: {
      "OK": function() {
        $(this).dialog("close");
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(currentMap);
        }
      },
    },
    open: function() {
        $('.ui-dialog-buttonpane').find('button:contains("OK")').addClass("OKButton");
        $('.withdraw').click(function() {
          $.post("mapgether/drop", {userid:userid, eventid:id})
            .done(function(data) {
              var list = $('#showAttendUser');
              list.empty();
              var attends = list.data('users');
              attends[userid] = undefined;
              list.append('<span class="plan-friend">Participant: </span>');
              for (var i = 1; i < attends.length; i++) {
                  if(typeof(attends[i]) != "undefined")
                      list.append(showAttendUser(attends[i]));
              }
              list.data('users',attends);   
              $('.join').show();
              $('.withdraw').hide();
              $('#eventdata_' + id).data('isattending', false);
            });
        });
        $('.join').click(function() {
          $.post("/mapgether/join", {userid:userid, eventid:id})
            .done(function(data) {
              var list = $('#showAttendUser');
              var attends = [];
              attends = list.data('users');
              attends[userid] = useraccount;
              list.append(showAttendUser(attends[userid]));
               
              // TODO: update attend user list
              $('.join').hide();
              $('.withdraw').show();
              $('#eventdata_' + id).data('isattending', true);
            });
        });
        $('.edit').click(function() {
            window.location.href='/mapgether/edit-event/'+id;
        });
        $('#add-comment').click(function() {
          var commentField = $('#comment_event_'+id)
          $.post("/mapgether/addcomment/"+id, {text:commentField.val()})
            .done(function(data) {

              //show comment
              data = JSON.parse(data);
              var comments = JSON.parse(data['comments']);
              // show the comments
              var list = $('#show-comment');
              list.html('');

              for (var i = 0; i < comments.length; i++){
                var comment = comments[i];
                var new_comment = $(comment.fields.html_comment);

                //new_comment.data("comment-id", comment.id);
                list.append(new_comment);
              }

            });
        });
        $.get("/mapgether/addcomment/"+id)
          .done(function(data) {

            data = JSON.parse(data);
            var comments = JSON.parse(data['comments']);
            // show the comments
            var list = $('#show-comment');

            //debug_info = comments;

            list.html('');

            for (var i = 0; i < comments.length; i++){
              var comment = comments[i];
              var new_comment = $(comment.fields.html_comment);

              //new_comment.data("comment-id", comment.id);
              list.append(new_comment);
            }

          });
        $.get("/mapgether/get-attenduser", {userid:userid, eventid:id})
            .done(function(data) {

            data = JSON.parse(data);
            data['attendusers'] =  JSON.parse(data['attendusers']);
            var list = $('#showAttendUser');
            list.append('<span class="plan-friend">Participant: </span>');
            var attendList = [];
            for (var user in data['attendusers']) {
                var e = data['attendusers'][user]['fields'];
                var pk = data['attendusers'][user]['pk'];
                list.append(showAttendUser(e.username)); 
                attendList[pk]=e.username;
            }
            $('#showAttendUser').data('users', attendList);
        });
        $.get("/mapgether/get-tagnames", {userid:userid, eventid:id})
            .done(function(data) {

            data = JSON.parse(data);
            var list = $('#showTagNames');
            list.append('<span class="plan-friend">Tags: </span>');
            for (var tag in data['tags']) {
                var e = data['tags'][tag]
                list.append(showTagName(e)); 
            }
        });
      },
   });
  //another way to show dialog
  //favDialog.showModal();
  $("#dialog-form").dialog("open");
}

function tagEventMap(name) {
  newMap('/mapgether/new-tag-event-map/' + name);
}

function specificEventMap(name) {
  newMap('/mapgether/new-specific-event-map/' + name);
}

function allEventMap() {
  newMap('/mapgether/new-map');
}

function newMap(url) {
  $.get(url)
  .done(function(data) {
    data = JSON.parse(data);
    var center = {lat: data['center-lat'], lng: data['center-lng']};
    var flag = false;
    if (data['user'].length != 0) {
      data['name'] = JSON.parse(data['user']);
      //alert("dghdfgh:"+data['name'][0]['fields']['username']);
      flag = true;
    }

    var map = new google.maps.Map($("#map")[0], {zoom: 15, center: center});
    currentMap = map;
    data['events'] = JSON.parse(data['events'])
    // for each event, create marker and show event info
    // clear event
    $("#events").empty()
    for (var event in data['events']) {
      var e = data['events'][event]['fields'];
      var position = {lat: parseFloat(e['latitude']), lng: parseFloat(e['longitude'])}

      // Set center at the first event's location.
      if (event == 0) {
        map.setCenter(position);
      }

      var marker = new google.maps.Marker({
        position: position,
        map: map,
        id: data['events'][event]['pk']
      });
      markers.push(marker);

      if (data['name']) {
        var currentUserId = data['name'][0].pk;
        var currentUserName = data['name'][0]['fields'].username;
      }
      var isOwner = currentUserId == e['owner'];
      var isAttending = e['attenduser'].indexOf(currentUserId) != -1;

      // add event
      $("#events").append(showEventHTML(data['events'][event]['pk'], e, flag, e['latitude'], e['longitude'], isOwner, isAttending, currentUserId, currentUserName));

      // marker.onclick
      marker.addListener('click', function() {
        var position = this.getPosition();
        map.setCenter(position);
        lat = position.toUrlValue(7).split(',')[0];
        longt = position.toUrlValue(7).split(',')[1];

        // hide events not in this location and show others
        childs = $("#events").children();
        var e = 0;
        while (e < childs.length) {
          saved_lat = $('#' + childs[e].id).data("lat");
          saved_longt = $('#' + childs[e].id).data("longt");
          if (saved_lat != lat || saved_longt != longt) {
            $('#' + childs[e].id).hide();
          } else {
            $('#' + childs[e].id).show();
          }
          e++;
        }
      });
    }
  });
}

function run_search(event) {
  event.preventDefault();
  prefix = $('#search_box').val()[0];
  name = $('#search_box').val().slice(1);
  if (prefix == '#') {
    tagEventMap(name);
  } else if (prefix == '@') { // redirect to user profile
    window.location.replace("/mapgether/linkProfile/" + name);
  } else if (prefix == '~') {
    specificEventMap(name);
  } else { // clear
    $('#search_box').value = '';
  }
}

function tag_event(event) {
  event.preventDefault();
  tagEventMap(this.id);
}

function getUpdates() {
   $.get("/mapgether/update-notification")
       .done(function(data) {
            data = JSON.parse(data);
            var list = $('#eventNotification');
            if (!!!data['events']) {
              return;
            }
            data['events'] = JSON.parse(data['events']);
            str_events = [];
            for (var event in data['events']) {
                var pk = data['events'][event]['pk'];
                var e = data['events'][event]['fields'];
                if (e.modified.substring(0,18) == e.created.substring(0,18)) {
                    str_events[pk] = "New Event:".concat(e.title);
                } else {
                    str_events[pk] = "Event Updated:".concat(e.title);
                }
            }
            list.empty();
            list.data('events',str_events);   
            list.append(eventNotification((data['events'].length))); 
        });
}

$(document).ready(function () {
  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  populate();
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    error: function(xhr, status, error) {
        console.log("An AJAX error occured: " + status + "\nError: " + error);
    }
  });

  $("#events").on('click', 'button.btn', zoomout);
  $("#run_search").on('click', run_search);
  $(".usertags").on('click', tag_event);
  window.setInterval(getUpdates, 5000);
  $("#eventNotification").on('click', 'button.btn', popout);
});
