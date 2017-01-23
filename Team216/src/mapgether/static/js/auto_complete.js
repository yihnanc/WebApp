function split(val) {
  return val.split(/,\s*/);
}

function extractLast(term) {
  return split(term).pop();
}

$(function() {
  $("#tags")
    // don't navigate away from the field on tab when selecting an item
    .on("keydown", function(event) {
      if (event.keyCode === $.ui.keyCode.TAB &&
        $(this).autocomplete("instance").menu.active) {
        event.preventDefault();
      }
    })
    .autocomplete({
    source: function(request,response) {
      $.getJSON("/mapgether/get-tags/", {
        term: extractLast(request.term)
      }, response);
    },
    focus: function() {
      // prevent value inserted on focus
      return false;
    },
    select: function(event, ui) {
      var terms = split(this.value);
      // remove the current input
      terms.pop();
      // add the selected item
      terms.push(ui.item.value);
      // add placeholder to get the comma-and-space at the end
      terms.push("");
      this.value = terms.join(", ");
      return false;
    }
  });

  $("#attenduser")
    // don't navigate away from the field on tab when selecting an item
    .on("keydown", function(event) {
      if (event.keyCode === $.ui.keyCode.TAB &&
        $(this).autocomplete("instance").menu.active) {
        event.preventDefault();
      }
    })
    .autocomplete({
    source: function(request,response) {
      $.getJSON("/mapgether/get-usernames/", {
        term: extractLast(request.term)
      }, response);
    },
    focus: function() {
      // prevent value inserted on focus
      return false;
    },
    select: function(event, ui) {
      var terms = split(this.value);
      // remove the current input
      terms.pop();
      // add the selected item
      terms.push(ui.item.value);
      // add placeholder to get the comma-and-space at the end
      terms.push("");
      this.value = terms.join(", ");
      return false;
    }
  });

  $("#search_box")
    // don't navigate away from the field on tab when selecting an item
    .on("keydown", function(event) {
      if (event.keyCode === $.ui.keyCode.TAB &&
        $(this).autocomplete("instance").menu.active) {
        event.preventDefault();
      }
    })
    .autocomplete({
    source: function(request,response) {
      $.getJSON("/mapgether/search/", {
        term: request.term
      }, response);
    },
    focus: function() {
      // prevent value inserted on focus
      return false;
    },
    select: function(event, ui) {
      this.value = ui.item.value;
      return false;
    }
  });
});
