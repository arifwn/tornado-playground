// Generated by CoffeeScript 1.3.3
(function() {
  var get_cookie;

  window.chatbox = {};

  $(document).ready(function() {
    console.log("ready");
    $("#chatname").focus();
    $("#chatform").on("submit", function() {
      var message, name;
      name = $("#chatname").val().trim();
      message = $("#chatmessage").val().trim();
      if ((message.length > 0) && (name.length > 0)) {
        $("#chatmessage").val("");
        chatbox.send(name, message);
      }
      $("#chatmessage").focus();
      return false;
    });
    return poll_message();
  });

  window.chatbox.append = function(name, message) {
    $('#chatlist > tbody:last').append("<tr><td><b>" + name + "</b></td><td>" + message + "</td></tr>");
    $("html, body").stop();
    return $("html, body").animate({
      scrollTop: $(document).height()
    }, 1500);
  };

  window.chatbox.send = function(name, message) {
    var data;
    data = {};
    data['name'] = name;
    data['message'] = message;
    $.postJSON("/cometnewmessage", data, function(response) {
      return console.log(response);
    });
    return console.log(name, ":", message);
  };

  window.jQuery.postJSON = function(url, args, callback) {
    $("#message-status-text").html("sending...");
    args._xsrf = get_cookie("_xsrf");
    return $.ajax({
      url: url,
      data: $.param(args),
      dataType: "text",
      type: "POST",
      success: function(response) {
        if (callback) {
          callback(response);
        }
        return $("#message-status-text").html("sent");
      },
      error: function(response) {
        console.log("ERROR:", response);
        return $("#message-status-text").html("failed");
      }
    });
  };

  window.poll_message = function() {
    console.log("start polling...");
    return $.ajax({
      url: "/cometmessage",
      type: "GET",
      success: function(response) {
        chatbox.append(response["name"], response["message"]);
        window.setTimeout(window.poll_message, 0);
        return $("#polling-status-text").html("ready");
      },
      error: function(response) {
        console.log(response);
        window.setTimeout(window.poll_message, 1000);
        return $("#polling-status-text").html("reconnecting...");
      }
    });
  };

  get_cookie = function(name) {
    var r;
    r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    if (r != null) {
      return r[1];
    } else {
      return void 0;
    }
  };

}).call(this);
