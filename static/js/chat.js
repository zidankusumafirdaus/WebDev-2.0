$(document).ready(function () {
    var socket = io.connect("http://localhost:5000");
    var currentRoom = "room1";
    var configElement = document.getElementById('config');
    var Dash = configElement.getAttribute("url");
    var username = configElement.getAttribute('data-username');

    socket.on("connect", function () {
        socket.emit("join", { username: username, room: currentRoom });
    });

    socket.on("message", function (data) {
        if (data.timestamp && data.username && data.text) {
            // Create the main message element
            const messageElement = $("<div>").addClass("message");
            const bubbleElement = $("<div>").addClass("bubble");
            const contentTextElement = $("<div>").addClass("content-text");
            const usernameElement = $("<div>").addClass("username").text(data.username);
            const textElement = $("<div>").addClass("text").text(data.text);
            contentTextElement.append(usernameElement, textElement);
            const timestampElement = $("<div>").addClass("timestamp").text(data.timestamp);
            
            bubbleElement.append(contentTextElement, timestampElement);
            
            messageElement.append(bubbleElement);
            
            if (data.username === username) {
                messageElement.addClass("self");
            } else {
                messageElement.addClass("other");
            }
            
            // Append the complete message to the messages container
            $("#messages").append(messageElement);
            
            // Scroll to the bottom of the messages container
            $("#messages").scrollTop($("#messages")[0].scrollHeight);
        }
    });
    

    $("#sendBtn").on("click", sendMessage);

    $("#message").on("keypress", function (e) {
        if (e.which == 13) {
            sendMessage();
        }
    });

    $("#leaveBtn").on("click", function () {
        socket.emit("leave", { username: username, room: currentRoom });
        socket.disconnect();
        window.location.href = Dash;
    });

    $(".room-item").on("click", function() {
        const newRoom = $(this).text().toLowerCase().replace(" ", "");
        socket.emit("leave", { username: username, room: currentRoom });
        socket.emit("join", { username: username, room: newRoom });
        currentRoom = newRoom;
        $("#current-room").text($(this).text());
        $("#messages").empty();
    });

    function sendMessage() {
        if ($("#message").val().trim() !== "") {
            socket.send({
                username: username,
                message: $("#message").val()
            });
            $("#message").val("");
        }
    }
});
