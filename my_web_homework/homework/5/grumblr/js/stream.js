function populateList() {
    $.get("/grumblr/get-streams")
      .done(function(data) {
          var list = $("#post-list");
          list.data('max-time', data['max-time']);
          list.html('')
          for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("post-id", post.id);
              list.append(new_post);
          }
      });
}


function addItem(){
    var postField = $("#post-field");
    //val means attribute value of input tag <input type= , value=>
    //call to add-tem in view.py, {post: xxx} is used to transmitted to view.py
    $.post("/grumblr/add-post", {post: postField.val()})
      .done(function(data) {
          getUpdates();
          postField.val("").focus();
     });
}


function getUpdates() {
    var list = $("#post-list")
    var max_time = list.data("max-time")
    //please review url.py, use attribute:max-time in html tag as the arg
    $.get("/grumblr/get-streams/"+ max_time)
      .done(function(data) {
          //data is the newest items  returned from get_changes in view.py    
        list.data('max-time', data['max-time']);
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var new_post = $(post.html);
            //add an attribute item-id in html tag and save item.id into it   
            new_post.data("post-id", post.id);
            list.append(new_post);
        }
      });
}

$(document).ready(function () {
  // Add event-handlers
  $("#add-post").click(addItem);
  //13 means enter(ASCII)
  $("#post-field").keypress(function (e) { if (e.which == 13) addItem(); } );
  $("#todo-list").click(deleteItem);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  $("#post-field").focus();

  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);

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
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
