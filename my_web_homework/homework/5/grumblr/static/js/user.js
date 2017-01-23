function populateList() {
    var name = $("#edit").attr("name");    
    var max_time = "1970-01-01T00:00+00:00";
    //please review url.py, use attribute:max-time in html tag as the arg
    $.get("/grumblr/get-userStreams/"+name+"/"+max_time) 
      .done(function(data) {
           var list = $("#edit");
           list.data('max-time', data['max-time']);
           list.html('')
           for (var i = 0; i < data.posts.length; i++) {
              post = data.posts[i];
              var new_post = $(post.html);
              new_post.data("postId", post.id);
              list.prepend(new_post);
              getNewComment(post.id);
          }
      });
}


function getUpdateStream() {
    var list = $("#edit");     
    var name = list.attr("name");    
    var max_time = list.data("max-time")
    //please review url.py, use attribute:max-time in html tag as the arg
    $.get("/grumblr/get-userStreams/"+name+"/"+max_time) 
      .done(function(data) {
           list.data('max-time', data['max-time']);
           for (var i = 0; i < data.posts.length; i++) {
              var post = data.posts[i];
              var new_post = $(post.html);
              //add an attribute item-id in html tag and save item.id into it   
              new_post.data("postId", post.id);
              list.prepend(new_post);
          }
      });
}

function addComment(e){
    var id = $(e.target).parent().data("postId");
    var commentField = $(e.target).parent().find("input")
    $.post("/grumblr/add-comment", {id:id, comment:commentField.val()})
      .done(function(data) {
          getNewComment(id);
          commentField.val("").focus();
     });
}

function getNewComment(postid) {
    var list = $("#item_"+postid)
    var max_time = list.data("max-time")
    if(max_time === undefined || max_time == "")
        max_time = "1970-01-01T00:00+00:00";
    //please review url.py, use attribute:max-time in html tag as the arg
    $.get("/grumblr/get-comments/"+ postid+"/"+max_time)
      .done(function(data) {
        list.data('max-time', data['max-time']);
        for (var i = 0; i < data.comments.length; i++) {
            var comment = data.comments[i];
            var new_comment = $(comment.html);
            //add an attribute item-id in html tag and save item.id into it
            list.append(new_comment);
        }
      });
}
$(document).ready(function () {
  // Add event-handlers
  //$("#add-btn").click(addItem);
  //13 means enter(ASCII)
  //$("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );
  //$("#todo-list").click(deleteItem);
  $("#edit").delegate("button", "click", addComment);

  // Set up to-do list with initial DB items and DOM data
  populateList();

  // Periodically refresh to-do list
  window.setInterval(getUpdateStream, 5000);

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
