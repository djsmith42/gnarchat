var inputBox = $("#chat-input")
var chatRoom = $("#chat-room")


function refreshChatMessages() {
	chatRoom.empty()
	$.getJSON("/messages", function(messages) {
		messages.forEach(function(message) {
			chatRoom.append("<div>" + message.author_name + ": " + message.text + "</div>")
		})
	})
}

inputBox.keypress(function(event) {
	if (event.which == 13) {
		console.log("Enter pressed!")
		$.ajax("/post_message",	{
			contentType: "application/json",
			type: "POST",
			data: JSON.stringify({
				text: inputBox.val(),
				author_name: "my name"
			})
		}).then(function() {
			refreshChatMessages()
		})
		inputBox.val('')
	}
});

refreshChatMessages()