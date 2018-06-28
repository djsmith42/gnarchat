var inputBox = $("#chat-input")
var chatRoom = $("#chat-room")

function refreshChatMessages() {
  // Fetch chat messages from the server:
	$.getJSON("/messages", function(messages) {
    // Build an HTML string that contains all the messages we got from the server:
    var html = ""
		messages.forEach(function(message) {
      html += ("<div><b>" + escape(message.author_name) + "</b>: " + escape(message.text) + "</div>")
		})
    // Replace all the HTML in the chat room box with the new HTML:
    chatRoom.html(html)
	})
}

// This function converts special HTML characters into safe characters,
// so baddies can't make our application execute their nasty code by
// posting chat messages with special HTML characters
function escape(text) {
  return $("<div>").text(text).html()
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
