
# our namespace
window.chatbox = {}

$(document).ready(() ->
    console.log "ready"
    
    chatbox.socket = socket_connect()
    
    $("#chatname").focus()
    
    $("#chatform").on("submit", () ->
        name = $("#chatname").val().trim()
        message = $("#chatmessage").val().trim()
        
        if (message.length > 0) and (name.length > 0)
            $("#chatmessage").val("")
            chatbox.send name, message
        
        $("#chatmessage").focus()
        return false
    )
    
)

socket_connect = () ->
    $("#polling-status-text").html("connecting...")
    socket = new WebSocket("ws://localhost:8000/messagesocket")
    socket.onopen = socket_on_open
    socket.onclose = socket_on_close
    socket.onerror = socket_on_error
    socket.onmessage = socket_on_message
    return socket

socket_on_message = (e) ->
    data = JSON.parse(e.data)
    window.chatbox.append data.name, data.message
    
socket_on_open = () ->
    $("#socket-status-text").html("ready")

socket_on_close = () ->
    # reconnect immediately
    $("#socket-status-text").html("closed. connecting...")
    chatbox.socket = socket_connect()
    
socket_on_error = () ->
    # reconnect immediately
    $("#socket-status-text").html("error. connecting...")
    chatbox.socket = socket_connect()

window.chatbox.append = (name, message) ->
    # append message to chatbox
    $('#chatlist > tbody:last').append "<tr><td><b>#{ name }</b></td><td>#{ message }</td></tr>"
    
    # scroll page to bottom
    $("html, body").stop()
    $("html, body").animate(
        scrollTop: $(document).height()
    , 1500)
    
window.chatbox.send = (name, message) ->
    # send message to server
    $("#message-status-text").html("sending...")
    data = {}
    data['name'] = name
    data['message'] = message
    data_json = JSON.stringify(data)
    chatbox.socket.send(data_json)
    console.log name, ":", message
    $("#message-status-text").html("sent")
