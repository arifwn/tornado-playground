// Generated by CoffeeScript 1.3.3
(function() {
  var socket_connect, socket_on_close, socket_on_error, socket_on_message, socket_on_open;

  window.chatbox = {};

  $(document).ready(function() {
    console.log("ready");
    chatbox.socket = socket_connect();
    $("#chatname").focus();
    return $("#chatform").on("submit", function() {
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
  });

  socket_connect = function() {
    var socket;
    $("#polling-status-text").html("connecting...");
    socket = new WebSocket("ws://localhost:8000/messagesocket");
    socket.onopen = socket_on_open;
    socket.onclose = socket_on_close;
    socket.onerror = socket_on_error;
    socket.onmessage = socket_on_message;
    return socket;
  };

  socket_on_message = function(e) {
    var data;
    data = JSON.parse(e.data);
    return window.chatbox.append(data.name, data.message);
  };

  socket_on_open = function() {
    return $("#socket-status-text").html("ready");
  };

  socket_on_close = function() {
    $("#socket-status-text").html("closed. connecting...");
    return chatbox.socket = socket_connect();
  };

  socket_on_error = function() {
    $("#socket-status-text").html("error. connecting...");
    return chatbox.socket = socket_connect();
  };

  window.chatbox.append = function(name, message) {
    $('#chatlist > tbody:last').append("<tr><td><b>" + name + "</b></td><td>" + message + "</td></tr>");
    $("html, body").stop();
    return $("html, body").animate({
      scrollTop: $(document).height()
    }, 1500);
  };

  window.chatbox.send = function(name, message) {
    var data, data_json;
    $("#message-status-text").html("sending...");
    data = {};
    data['name'] = name;
    data['message'] = message;
    data_json = JSON.stringify(data);
    chatbox.socket.send(data_json);
    console.log(name, ":", message);
    return $("#message-status-text").html("sent");
  };

}).call(this);
