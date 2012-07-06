
# our namespace
window.chatbox = {}

$(document).ready(() ->
    console.log "ready"
    
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
    
    poll_message();
)

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
    
    data = {}
    data['name'] = name
    data['message'] = message
    $.postJSON("/cometnewmessage", data, (response) ->
        console.log response
    )
    console.log name, ":", message

window.jQuery.postJSON = (url, args, callback) ->
    $("#message-status-text").html("sending...")
    args._xsrf = get_cookie("_xsrf")
    $.ajax(
        url: url
        data: $.param(args)
        dataType: "text"
        type: "POST"
        success: (response) ->
            if (callback)
                callback(response)
            $("#message-status-text").html("sent")
        error: (response) ->
            console.log "ERROR:", response
            $("#message-status-text").html("failed")
    )


window.poll_message = () ->
    console.log "start polling..."
    
    $.ajax(
        url: "/cometmessage"
        type: "GET"
        success: (response) ->
            chatbox.append response["name"], response["message"]
            window.setTimeout(window.poll_message, 0)
            $("#polling-status-text").html("ready")
        error: (response) ->
            console.log response
            window.setTimeout(window.poll_message, 1000)
            $("#polling-status-text").html("reconnecting...")
    )

get_cookie = (name) ->
    r = document.cookie.match("\\b#{ name }=([^;]*)\\b")
    
    if r?
        return r[1]
    else
        return undefined
    